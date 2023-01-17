#%%
from cleaning_dataset.ClientProcessingCleaning.ClientProcessingCleaning import Processing, Cleaning
from unittest import mock, TestCase
import pandas as pd

@mock.patch('pandas.read_csv', return_value = pd.DataFrame({'a':[1,2,3,4,None],
                                                       'b':['a','b','c','d',None]}) )
class SimpleValidationsTest(TestCase):
    def test_validating_nan_values(self, pandas_read):
        df = pd.read_csv()
        df = df.dropna()
        self.assertEqual(len(df), 4)

    def test_len_of_df(self, pandas_read):
        df = pd.read_csv()
        processing_config = [('b','\D+')]
        self.assertEqual(len(df), 5)
        self.assertFalse(False in df.a)
        df = df.dropna()
        self.assertTrue(not False in df.a)
        for config in processing_config:
            df = Processing.filtering_columns_by_regex(df, config)
        self.assertFalse(any(df.b))