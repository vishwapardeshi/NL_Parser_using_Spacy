from bs4 import BeautifulSoup #scraping
import requests #for HTTP requests
import re
import pandas
import sys
import os
import pandas as pd

import logging

logging.basicConfig(level=logging.DEBUG)

class Crawler():
    def __init__(self):
        self.base_url = 'https://www.allrecipes.com/recipes/?page='

    def get_links(self, num_pages):
        if num_pages <= 0:
            raise ValueError("The number of pages scraped should be more than 0. Got non-positive number instead!")

        if not isinstance(num_pages, int):
            raise ValueError("The number of pages scraped should be a positive integer. Got decimal instead!")

        recipe_list = []
        for page in range(1, int(num_pages) + 1):
            r = requests.get(self.base_url + str(page))
            html = BeautifulSoup(r.content, 'html.parser')
            num_recipes = 0
            for recipe in html.findAll('article', {'class' : 'fixed-recipe-card'}):
                link = recipe.find("a", attrs={'href': re.compile(r"^https://www.allrecipes.com/recipe")})
                name = recipe.find('span', {"class":"fixed-recipe-card__title-link"}).text
                recipe_list.append({"name" : name, "url" : link['href']})
                num_recipes += 1
            print("Extracted {0} recipes from page {1}".format(num_recipes, page))
        return recipe_list

    def get_content(self, recipe_link_list):
        for ix in range(len(recipe_link_list)):
            url = recipe_link_list[ix]['url']
            r = requests.get(url) #returns a variable which contains the html doc unstructured
            currRecipe = BeautifulSoup(r.content, "html.parser")
            #there are two versions of the website, the old and new have different html structure
            #they require different parsing
            ver = -1
            if currRecipe.find_all('ul', {'class':'ingredients-section'}):
                ingrd_content  = currRecipe.find_all('ul', {'class':'ingredients-section'})
                ver = 0
            else:
                ingrd_content = currRecipe.findAll('ul', {'id':re.compile('^lst_ingredients')})
                ver = 1
            currIngredient = self.get_ingredients(ver,ingrd_content)
            recipe_link_list[ix]['ingredients'] = currIngredient
            print("\r", "Adding {0} ingredients to {1} recipe".format(len(currIngredient), ix + 1))
        return(recipe_link_list)


    def get_ingredients(self, version, content):
        ingredient_list = []
        if version == 0:
          attrs = {'class':'ingredients-item'}
        elif version == 1:
          attrs = {'class':"checkList__line"}
        else:
            return ingredient_list
        for ul in content:
          for li in ul.findAll('li', attrs):
            ingredient = li.find("span").text.encode('utf-8').strip() #basic stripping to eliminate whitespaces
            if ingredient != "Add all ingredients to list": #sometimes this is read in too
              ingredient_list.append(ingredient)
        return(ingredient_list)

    def convert_to_dataframe(self, recipe_list):
        if len(recipe_list[0]) < 3:
            return pd.DataFrame(columns = ['url', 'name', 'ingredient'])

        base_df = pd.DataFrame(recipe_list)
        ingredient = base_df.apply(lambda x: pd.Series(x['ingredients']), axis=1).stack().reset_index(level=1, drop=True)
        ingredient.name = 'ingredient'
        recipes_df= base_df.drop('ingredients', axis=1).join(ingredient)
        recipes_df['ingredient'] = pd.Series(recipes_df['ingredient'], dtype=object)
        recipes_df.reset_index(inplace = True,drop='index')
        recipes_df = recipes_df[['url', 'name', 'ingredient']]
        return recipes_df

    def save_data(self, df, filepath):
        """
        Takes clean dataframe from `convert_to_dataframe` and saves it as csv

        :Input:
            :train_df: Clean data frame from `convert_to_dataframe`
            :clean_filename: String, csv file name
        :Returns:
            :None: Does not return anything but saves the csv file
        """
        if os.path.isfile(filepath):
            df.to_csv(filepath, mode='a', header=False)
        else:
            df.to_csv(filepath, index = False, header = True)

def main():
    if len(sys.argv) == 4:

        num_pages, dir_path, filepath = sys.argv[1:]

        print('Scraping website for recipe link...\n    Pages: {}'
              .format(num_pages))

        crawler = Crawler()
        #print(crawler)
        recipe_link_list = crawler.get_links(int(num_pages))

        print('Cleaning data...')
        recipe_list = crawler.get_content(recipe_link_list)

        print('Saving data...\n    CSV: {}'.format(os.path.join(dir_path, filepath + '.csv')))
        df = crawler.convert_to_dataframe(recipe_list)

        crawler.save_data(df, os.path.join(dir_path, filepath + '.csv'))

        print('Cleaned data saved to csv file!')
    else:
        print("'Please provide the number of webpages to scrape and\
        directory and filename of the csv file to save the scraped data\
         \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db'")

if __name__ == '__main__':
    main()
