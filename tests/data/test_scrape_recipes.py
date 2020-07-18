import os
import numpy as np
import pytest
import sys

from data.scrape_recipes import get_recipe_links, get_ingredients, get_each_recipe

class TestGetRecipeLinks(object):
    def test_valueerror_on_negative_recipe_number(self):
        pass

class TestGetIngredients(object):
    def test_valueerror_on_incorrect_version(self):
        pass

class TestGetEachRecipe(object):
    def test_empty_list(self):
        pass
