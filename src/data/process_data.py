from collections import defaultdict
import os
import sys
import numpy as np
import pandas as pd
import re
import math

def load_data(dir_path, train_data_filepath):
    """
        Load training data from the csv.
    Args:
        dir_path: the directory containing train data
        train_data_filepath: the path of the ny_times_recipe.csv file which is used for training
    Returns:
        train_df (DataFrame): Dataframe containing annonated data
    """
    #load data
    if not os.path.isfile(os.path.join(dir_path, train_data_filepath)):
        raise FileNotFoundError("This file doesn't exist")
    else:
        train_df = pd.read_csv(os.path.join(dir_path,train_data_filepath))
        return train_df

def clean_data(train_df, stopwords_filepath):
    """
    Takes loaded data frame from `load_data` and cleans it for use.

    Args
        train_df: Data frame created from `load_data`
        stopwords_filepath: the path of stopwords.txt
    Returns:
        train_df: Cleaned data frame.
    """
    #convert input and name to string
    train_df['input'] = train_df['input'].astype(str)
    train_df['ingredient_name'] = train_df['name'].astype(str)

    #drop null values
    train_df = train_df.dropna(axis = 0, subset = ['input', 'ingredient_name'])

    #load stopwords
    with open(stopwords_filepath) as f:
        stopwords = f.read().splitlines()
    #clean extra words and brackets from
    cleaned_ingredient = []
    for _, row in train_df.iterrows():
      #remove text within parantheses along with the parantheses
      row['ingredient_name'] = re.sub(r"[\(\[].*?[\)\]]", "", row['ingredient_name'])
      row['ingredient_name'] = row['ingredient_name'].replace("-", "")
      curr_row =  row['ingredient_name'].split()
      if len(curr_row) > 1:
        clean_words  = [word for word in curr_row if word.lower() not in stopwords]
        row['ingredient_name'] = ' '.join(clean_words)
      if row['ingredient_name'] == '':
        cleaned_ingredient.append(" ")
      else:
        cleaned_ingredient.append(row['ingredient_name'])

    train_df['ingredient_name'] = cleaned_ingredient

    #drop null values
    train_df = train_df.dropna(axis = 0, subset = ['input', 'ingredient_name'])

    return(train_df[['input', 'ingredient_name']])


def save_data(train_df, dir_path, clean_filename):
    """
    Takes clean dataframe from `clean_data` and saves it as a csv file

    Args
        train_df: Clean data frame from `clean_data`
        clean_filename: String, csv file name
    Returns:
        None: Does not return anything but saves the csv file
    """
    filename = os.path.join(dir_path, clean_filename + ".csv")
    train_df.to_csv(filename, index = False, header = True)


def transform_to_entity_map(line, ingredient_list, entity):
    """
    Takes ingredient description and converts it into an entity map

    Args
        line: String containing ingredient description
        ingredient_list: list of ingredient's present in line
        entity: String containing name of entity to be extracted; here ingredient
    Returns:
        curr_dict['entities']: returns data in spacy training data format for one line of ingredient
    """

    if entity != "INGREDIENT":
        raise ValueError("The entity type is limited to only INGREDIENT. Got {}!".format(entity))
    curr_dict = {}
    if len(ingredient_list) == 0:
        return []
    elif len(ingredient_list) == 1:
      ingd_regex = re.compile(ingredient_list[0])
      entity_match = ingd_regex.search(line)
      curr_dict['entities'] = [(entity_match.start(), entity_match.end(), entity)]
      return(curr_dict['entities'])
    else:
      for i in range(len(ingredient_list)):
        ingd_regex = re.compile(ingredient_list[i])
        entity_match = ingd_regex.search(line)
        if entity_match:
            element = (entity_match.start(), entity_match.end(), entity)
            if i == 0:
              curr_dict['entities'] = [element]
            elif element not in curr_dict['entities']:

              curr_dict['entities'].append(element)
    return(curr_dict['entities'])


def generate_structured_train_data(clean_data_path, final_filename):
    """
    Generates and saves training data in format required for spacy NER model

    Args
        clean_data_path: filepath of the cleaned dataframe containing annonated data
        final_filename: file name to which the training data will be saved to
    Returns:
        train_data: returns list containing training_data formatted for spacy NER model
    """

    entity = 'INGREDIENT'
    #load the clean datasets
    df = pd.read_csv(clean_data_path)
    train_data = []
    subset = df[['input', 'ingredient_name']]
    for ix in range(len(df)):
      line = subset.iloc[ix, 0]
      ingd_name = subset.iloc[ix, 1]
      entity_dict = {}
      if ingd_name == 'nan':
          continue
      ingd_list = str(ingd_name).split()
      flag = 0
      #for each token
      for ingredient in ingd_list:
        if line == 'nan' or ingredient == 'nan':
          flag = 1
          continue
        if ingredient not in str(line) and flag == 0:
          flag = 1
          continue
      if flag == 0:
        entity_dict['entities'] = transform_to_entity_map(line, ingd_list, entity)
        train_data.append((line, entity_dict))
        print("\r", "Adding", (line, entity_dict), "to row {0}".format(ix + 1))
      else:
        print("\r","Skipping {} row".format(ix + 1))

    #create df
    with open(final_filename, 'w') as f:
        for item in train_data:
            f.write("{}\n".format(item))

    return(train_data)

def main():
    if len(sys.argv) == 4:

        data_path, clean_filename, final_filename = sys.argv[1:]

        external_data_path = os.path.join(data_path, 'external')
        interim_data_path = os.path.join(data_path, 'interim')
        proc_data_path = os.path.join(data_path, 'processed')

        print('Loading data...\n    EXTERNAL DATA: {}'
              .format(external_data_path, 'ny_times_recipe.csv'))
        train_df = load_data(external_data_path, 'ny_times_recipe.csv')

        print('Cleaning data...')
        train_df = clean_data(train_df, os.path.join(external_data_path, 'recipes_stopwords.txt'))

        print('Saving intermediate data...\n    CSV: {}'
            .format(os.path.join(interim_data_path, clean_filename)))
        save_data(train_df, interim_data_path, clean_filename)

        print('Cleaned data saved to folder!')

        print('Generated Entity Map & transforming data for model training...')
        print('Saving training data...\n    CSV: {}'
            .format(os.path.join(proc_data_path, final_filename + '.txt')))
        train_data = generate_structured_train_data(os.path.join(interim_data_path,\
         clean_filename + '.csv'),os.path.join(proc_data_path, final_filename + '.txt') )


    else:
        print('Please provide the directory path of data folder'\
              ' as well as the filename for cleaned and transformed data'\
              '\n\nExample: python process_data.py '\
              'data/ clean_train final_train')

if __name__ == '__main__':
    main()
