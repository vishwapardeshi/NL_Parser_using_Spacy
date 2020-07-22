import pytest
import pandas as pd
import pandas.testing as pdt

from data.process_scraped_data import (convert_vulgar_to_mixed_fraction)


class TestConvertVulgarToMixedFraction(object):
    def test_on_empty_dataframe(self):
        empty_dataframe = pd.DataFrame()
        with pytest.raises(ValueError) as exc_info:
            convert_vulgar_to_mixed_fraction(empty_dataframe)
        expected_error_msg = "The dataframe should have 3 columns - url, name, ingredient. Found {0}"
        assert exc_info.match(expected_error_msg)

    def test_on_non_unicode_data(self):
        one_unicode_df = pd.DataFrame([['xyc.com', 'Recipe A', '2 teaspoons smokehouse']], columns = ['url', 'name', 'ingredient'])
        expected = pd.DataFrame([['xyc.com', 'Recipe A', '2 teaspoons smokehouse']], columns = ['url', 'name', 'ingredient'])
        actual = convert_vulgar_to_mixed_fraction(one_unicode_df)
        pdt.assert_frame_equal(actual, expected)

    def test_on_correct_column_name(self):
        correct_col_df = pd.DataFrame([['Recipe A', '2 teaspoons smokehouse']], columns = ['name', 'ingredient'])
        expected = correct_col_df
        actual = convert_vulgar_to_mixed_fraction(correct_col_df)
        pdt.assert_frame_equal(actual, expected)
