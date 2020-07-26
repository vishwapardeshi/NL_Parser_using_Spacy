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
        test_filepath: the path of the test data csv file
    Returns:
        df: DataFrame containing test data
    """

    # load data from database
    #READ FROM CSV

    df = pd.read_csv(test_filepath)

    return(df)

def load_model(model_filepath):
    """
        Load trained model.
    Args:
        model_filepath: the path of the model pkl file
    Returns:
        model: Returns trained model
    """
    model = joblib.load(model_filepath)
    return model


def predict(df, model_filepath):
    """
      Extract ingredient name from description using custom named entity recognition model
    Args:
        df: test data DataFrame
        model_filepath: the path of the trained model pkl file
    Returns:
        clean_ingredients: list containing extracted entities
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
    """
      Save the predicted/extracted values
    Args:
        df: test data DataFrame
        predicted_values: values generated using the trained model on the test data
        filepath: the path where the predicted values are to be stored
    Returns:
        None: Returns none but saves the csv to the filepath
    """
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
        print('Please provide the filepath of the model & test data '\
              'and name of the test_file and the predicted_file name by which to '\
              'store the results. \n\nExample: python3 '\
              'predict.py model/model.pkl data/processed final_test_data predicted_test')


if __name__ == '__main__':
    main()
