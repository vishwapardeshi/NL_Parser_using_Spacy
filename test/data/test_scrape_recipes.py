import os
import numpy as np
import pytest
import sys

from data.scrape_recipes import Crawler


class TestGetLinks(object):
    crawler = Crawler('https://www.allrecipes.com/recipes/?page=')
    def test_valueerror_on_negative_recipe_number(self):
        with pytest.raises(ValueError) as exc_info:
            self.crawler.get_links(-1)
        expected_error_msg = "The number of pages scraped should be more than 0. Got non-positive number instead!"
        assert exc_info.match(expected_error_msg)

    def test_valueerror_on_incorrect_data_type(self):
        with pytest.raises(ValueError) as exc_info:
            self.crawler.get_links(2.2)
        expected_error_msg = "The number of pages scraped should be a positive integer. Got decimal instead!"
        assert exc_info.match(expected_error_msg)

    def test_on_one_page(self):
        actual_len = len(self.crawler.get_links(1))
        assert actual_len > 0, "Expected length: > 0, Actual length: {0}".format(actual_len)


class TestGetIngredients(object):
    def test_valueerror_on_incorrect_version(self):
        pass

class TestContent(object):
    def test_incorrect_version(self):
        pass

class TestConvertToDataFrame(object):
    def test_column_name(self):
        pass
    def test_incomplete_recipe_list(self):
        pass
