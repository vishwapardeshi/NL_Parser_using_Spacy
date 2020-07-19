import os
import numpy as np
import pytest
import sys

from data.scrape_recipes import get_links, get_ingredients, get_each_recipe

class TestGetLinks(object):
    def test_valueerror_on_negative_recipe_number(self):
        with pytest.raises(ValueError) as exc_info:
            get_recipe_links(-1)
        expected_error_msg = "The number of pages scraped should be more than 0.\
        Got non-positive number instead!"
        assert exc_info.match(expected_error_msg)

    def test_valuerror_on_non_integer_recipe_number(self):
        with pytest.raises(ValueError) as exc_info:
            get_recipe_links(0.2)
        expected_error_msg = "The number of pages scraped should be a positive integer.\
        Got decimal instead!"
        assert exc_info.match(expected_error_msg)

    def test_empty_list(self):
        pass
    def test_expected(self):
        pass

class TestGetIngredients(object):
    def test_valueerror_on_incorrect_version(self):

        pass


    def test_

class TestGetEachRecipe(object):
    def test_empty_list(self):
        pass
