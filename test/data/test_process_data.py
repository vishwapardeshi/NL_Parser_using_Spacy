import pytest

from data.process_data import (clean_data, load_data, transform_to_entity_map, generate_structured_train_data)

class TestLoadData(object):
    def test_on_invalid_file(self):
        pass

class TestCleanData(object):
    def test_on_stopword(self):
        pass

    def test_columns_present(self):
        pass

    def test_empty_ingredient(self):
        pass

class TestTransformToEntityMap(object):
    def test_empty_ingredient_list(self):
        pass
    def test_on_single_ingredient(self):
        pass
    def test_on_repeating_ingredients(self):
        pass
    def test_entity_is_ingredient(self):
        pass

class TestGenerateStructuredTrainData(object):
    def test_empty_ingredient_string(self):
        pass
    def test_on_empty_ingredient_description(self):
        pass

#genertate generate_structured_train_data
#test_empty ingredient named

#empty linguine
