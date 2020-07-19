import sys
import pandas as pd
import numpy as np
import pickle


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


    return X, Y, category_names


def predict():
    """
      build NLP pipeline - count words, tf-idf, multiple output classifier,
      grid search the best parameters
    Args:
        None
    Returns:
        cross validated classifier object
    """
    #
    extracted = []
    for _,row in recipes_df.iterrows():
      nlp_ing = ner_model(row['ingredient'])
      ans = {}
      for ent in nlp_ing.ents:
        ans[ent.label_] = ent.text.lower()#once the ingredients are found convert to lower case
      extracted.append(ans)

     #generate list
     clean_ingredients = []
     for ix in range(len(recipes_df.ingredient)):
       curr = extracted[ix]
       if curr == {}:
         ingd = " "
       else:
         ingd = curr['INGREDIENT']
       clean_ingredients.append(ingd)

    return clean_ingredients



def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

        #convert to a new dataframe
        clean_recipe = recipes_df[['url', 'name']]
        clean_recipe['ingredient'] = clean_ingredient

        clean_recipe.head()

        clean_recipe.to_csv('cleanData.csv')



    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
def train_spacy(data,iterations):
    TRAIN_DATA = data
    nlp = spacy.load('en_core_web_sm')
    ner = nlp.get_pipe("ner")
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])
    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp

ner_model = train_spacy(TRAIN_DATA, 25)

#save to model
ner_model.to_disk('ner_model')
