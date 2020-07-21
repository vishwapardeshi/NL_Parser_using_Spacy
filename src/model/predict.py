import sys
import pandas as pd
import numpy as np
import pickle
import os

import joblib


def load_data(test_filepath):
    """
        Load data from csv file.
    Args:
        database_filepath: the path of the database file
    Returns:
        X (DataFrame): messages
        Y (DataFrame): One-hot encoded categories
        category_names (List)
    """

    # load data from database
    #READ FROM CSV

    df = pd.read_csv(test_filepath)

    return(df)

def load_model(model_filepath):
    return joblib.load(model_filepath)


def predict(df, model_filepath):
    """
      build NLP pipeline - count words, tf-idf, multiple output classifier,
      grid search the best parameters
    Args:
        None
    Returns:
        cross validated classifier object
    """
    #
    ner_model = load_model(model_filepath)
    extracted = []
    for _,row in df.iterrows():
      nlp_ing = ner_model(row['ingredient'])
      ans = {}
      for ent in nlp_ing.ents:
        ans[ent.label_] = ent.text.lower()#once the ingredients are found convert to lower case
      extracted.append(ans)

 #generate list
    clean_ingredients = []
    for ix in range(len(df.ingredient)):
        curr = extracted[ix]
        if curr == {}:
            ingd = " "
        else:
            ingd = curr['INGREDIENT']
        clean_ingredients.append(ingd)

    return clean_ingredients


def save_data(df, predicted_values, filepath):
        #convert to a new dataframe
        df = df[['url', 'name']]
        df['ingredient'] = predicted_values
        df.to_csv(filepath)

def main():
    if len(sys.argv) == 5:
        model_filepath, data_filepath, test_filename, predicted_filename = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(data_filepath))
        test_df = load_data(os.path.join(data_filepath, test_filename + '.csv'))

        print('Predicting values...')
        extracted_ingredients = predict(test_df, os.path.join(model_filepath, 'ner_model.pkl'))

        print('Saving values to the file')
        save_data(test_df, extracted_ingredients, os.path.join(data_filepath, predicted_filename + '.csv'))


    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
