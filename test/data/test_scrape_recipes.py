import os
import pandas as pd
import pytest
import sys
import pandas.testing as pdt

from data.scrape_recipes import Crawler


class TestGetLinks(object):
    crawler = Crawler()
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
    crawler = Crawler()
    def test_valueerror_on_incorrect_version(self):
        expected = []
        actual = self.crawler.get_ingredients(-1, "")
        assert actual == expected, "Expected: {0}, Actual: {1}".format(expected, actual)

class TestContent(object):
    crawler = Crawler()
    def test_empty_list(self):
        expected = []
        actual = self.crawler.get_content([])
        assert actual == expected, "Expected: {0}, Actual: {1}".format(expected, actual)

class TestConvertToDataFrame(object):
    crawler = Crawler()
    def test_column_name(self):
        df = pd.DataFrame([['1','1','1']], columns = ['url', 'name', 'ingredient'])
        expected = df
        actual = self.crawler.convert_to_dataframe([{'name': '1', 'url':'1', 'ingredients':['1']}])
        pdt.assert_frame_equal(actual, expected)

    def test_incomplete_recipe_list(self):
        df = pd.DataFrame(columns = ['url', 'name', 'ingredient'])
        expected = df
        actual = self.crawler.convert_to_dataframe([{'name': '1', 'url':'1'}])
        pdt.assert_frame_equal(actual, expected)
