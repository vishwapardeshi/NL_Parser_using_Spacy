import sys
import pandas as pd
import numpy as np
import pickle
import spacy

import random

def load_data(train_filepath):
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
    train_data = []
    with open(train_filepath) as f:
        content = f.read().splitlines()
        train_data = [eval(c) for c in content]
    return trim_entity_spans(train_data)

import re


def trim_entity_spans(data):
    """Removes leading and trailing white spaces from entity spans.

    Args:
        data (list): The data to be cleaned in spaCy JSON format.

    Returns:
        list: The cleaned data.
    """
    invalid_span_tokens = re.compile(r'\s')

    cleaned_data = []
    for text, annotations in data:
        entities = annotations['entities']
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]):
                valid_start += 1
            while valid_end > 1 and invalid_span_tokens.match(
                    text[valid_end - 1]):
                valid_end -= 1
            valid_entities.append([valid_start, valid_end, label])
        cleaned_data.append([text, {'entities': valid_entities}])

    return cleaned_data

def build_model():
    """
      build NLP pipeline - count words, tf-idf, multiple output classifier,
      grid search the best parameters
    Args:
        None
    Returns:
        cross validated classifier object
    """

    custom_ner = spacy.load('en_core_web_sm')
    ner_pipe = custom_ner.get_pipe("ner")
    if 'ner' not in custom_ner.pipe_names:
        ner_pipe = custom_ner.create_pipe('ner')
        custom_ner.add_pipe(ner_pipe, last=True)

    return (custom_ner, ner_pipe)

def fit(model, ner_pipe,  train_data, iterations):

    # add labels
    for _, annotations in train_data:
         for ent in annotations.get('entities'):
            ner_pipe.add_label(ent[2])
    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in model.pipe_names if pipe != 'ner']
    with model.disable_pipes(*other_pipes):  # only train NER
        optimizer = model.begin_training()
        for iteration in range(iterations):
            print("Statring iteration " + str(iteration))
            random.shuffle(train_data)
            losses = {}
            for text, annotations in train_data:
                model.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return model



def save_model(model, model_filepath):
    """
        Save model to pickle
    """
    joblib.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        data_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    TRAIN_DATA: {}'.format(data_filepath))
        train_data = load_data(data_filepath)
        print(train_data[:5])

        print('Building model...')
        ner_model, ner_pipe = build_model()

        print('Training model...')
        fit(ner_model, ner_pipe, train_data, 25)


        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(ner_model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
