import pytest
import os
import pandas as pd
import pandas.testing as pdt

from data.process_data import (clean_data, load_data, transform_to_entity_map, generate_structured_train_data)

@pytest.fixture
def stopword_file():
    file_path = "stopwords.txt"
    with open(file_path, "w") as f:
        f.write("ground\nto\ntaste\nand\nor\npowder\nwhite\nred\ngreen\nyellow\n")
    yield file_path
    os.remove(file_path)

class TestCleanData(object):
    df = pd.DataFrame([[4,"1 1/2 tablespoons vegetable oil","vegetable oil",1.5,0.0,"tablespoon",""],
    [5,"",'water',0.5,0.0,"cup",""]], columns = ['index', 'input', 'name', 'qty', 'range_end', 'unit', 'comment'])

    def test_empty_ingredient(self, stopword_file):
        expected =pd.DataFrame([["1 1/2 tablespoons vegetable oil","vegetable oil"],
        ['','water']], columns = ['input', 'ingredient_name'])
        actual = clean_data(self.df, stopword_file)
        pdt.assert_frame_equal(actual, expected), "Expected: {0}, Actual: {1}".format(expected, actual)


class TestTransformToEntityMap(object):
    def test_empty_ingredient_list(self):
        expected = []
        actual = transform_to_entity_map('abc', [], 'INGREDIENT')
        assert actual == expected, "Expected: {0}, Actual: {1}".format(expected, actual)

    def test_on_single_ingredient(self):
        expected = [(2, 8, 'INGREDIENT')]
        actual = transform_to_entity_map('2 tomato', ['tomato'], 'INGREDIENT')
        assert actual == expected, "Expected: {0}, Actual: {1}".format(expected, actual)

    def test_on_repeating_ingredients(self):
        expected = [(2, 8, 'INGREDIENT')]
        actual = transform_to_entity_map('2 tomato or tomatoes', ['tomato'], 'INGREDIENT')
        assert actual == expected, "Expected: {0}, Actual: {1}".format(expected, actual)

    def test_entity_is_ingredient(self):
        with pytest.raises(ValueError) as exc_info:
            transform_to_entity_map('abc', [], 'QUANT')
        expected_error_msg = "The entity type is limited to only INGREDIENT. Got QUANT!"
        assert exc_info.match(expected_error_msg)


@pytest.fixture
def clean_data_file():
    file_path = "clean.csv"
    with open(file_path, "w") as f:
        f.write("input,ingredient_name\n\"1 medium-size onion, peeled and chopped\",")
    yield file_path
    os.remove(file_path)

class TestGenerateStructuredTrainData(object):
    def test_empty_ingredient_string(self, clean_data_file):
        expected = []
        actual = generate_structured_train_data(clean_data_file, "save.txt")
        assert actual == expected, "Expected: {0}, Actual: {1}".format(expected, actual)

    def test_on_empty_ingredient_description(self, clean_data_file):
        expected = []
        actual = generate_structured_train_data(clean_data_file, "save.txt")
        assert actual == expected, "Expected: {0}, Actual: {1}".format(expected, actual)
