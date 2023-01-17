import numpy as np
import pandas as pd
import re
from scipy import stats
from matplotlib import pyplot as plt

class Processing:
    def __init__(self, df:pd.DataFrame):
        self.df = df

    def combining_similar_values_df(self, column:str, to_find_values:list or tuple) -> None:
        add_left:str = ''
        add_right:str = ''
        for to_find_value in to_find_values:
            if isinstance(to_find_value, str):
                self.df[column] = self.df[column].apply(lambda l: self.combine_similar_values(row_value=l, add_left=add_left, to_find_value=to_find_value, add_right=add_right))
            elif isinstance(to_find_value, tuple):
                self.df[column] = self.df[column].apply(lambda l: self.combine_similar_values(row_value=l, add_left=to_find_value[0], to_find_value=to_find_value[1], add_right=to_find_value[2]))

    def combine_similar_values(self, row_value:str, to_find_value:str, add_left:str='', add_right:str='') -> str:
        """
        input : 
            - row_value is the value received 
            - to_find_value is the value that will replaced the row value if conditions are meet
        tries to find similar values in a column, so it can group them
        output :
            - to_find_value if condition is meet
            - row_value if condition is not meet
        """
        if self.validating_similar_values(row_value, to_find_value):
            return add_left + to_find_value + add_right
        return row_value

    def validating_similar_values(self, row_value:str, to_find_value:str) -> bool:
        return row_value.startswith(to_find_value.strip()) or row_value.endswith(to_find_value.strip())

    def cleaning_columns(self, values:tuple=('column','regex') or dict, replace_value:str='') -> None:
        if isinstance(values, tuple):
            self.df[values[0]] = self.df[values[0]].astype(str).str.replace(values[1],replace_value, regex=True)
        elif isinstance(values, dict):
            column = list(values.keys())[0]
            self.df[column] = self.df[column].astype(str).str.replace(values[column],values['replace'], regex=True)

    def filtering_columns_by_regex(self, values:tuple=('column','regex')) -> None:
        if isinstance(values, tuple):
            self.df = self.df[self.df[values[0]].str.contains(values[1].lower())]
        elif isinstance(values, dict):
            self.df = self.df[self.df[values[0]].str.contains(values[1].lower())]

    def changing_values_with_tildes(self, column:str)  -> None:
        values_to_replace = {'á': 'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u'}
        for value in values_to_replace.keys():
            self.df[column] = self.df[column].astype(str).apply(lambda l: self.replacing_values(l, value, values_to_replace) )

    def replacing_values(self, row:str, value:str, values_to_replace:dict) -> str:
        return row.replace(value, values_to_replace[value])

    def unifying_categories(self, categories_to_unify:dict, column:str) -> None:
        values_to_unify = list(categories_to_unify.keys())
        self.df[column] = self.df[column].apply(lambda x: categories_to_unify[x] if x in values_to_unify else x)

    def punctual_process(self, column:str = 'rooms') -> None:
        self.df[column] = self.df[column].astype('str')
        #Sino aclaro la columna recorre todos uno por uno el apply
        #self.df[column] = self.df[column].apply(lambda l: str(int(re.sub('\D+', '', l.replace('Mono','0'))) + 1) if 'dorm' in l.split(' ')[-1] or 'Mono' in l.split(' ')[-1]  else l)
        self.df[column] = self.df[column].apply(lambda l: str(int(re.sub('\D+', '', l)) + 1) if 'dorm' in l.split(' ')[-1]  else l)
        self.df[column] = self.df[column].apply(lambda l: str(1) if 'Mono' in l.split(' ')[-1] else l)

    def segregating_by_fields(self, columns_to_segregate:dict) -> pd.DataFrame:
        for column, value in columns_to_segregate.items():
            self.df = self.df[self.df[column] == value]
        return self.df

class Cleaning:
    @staticmethod
    def generating_median_for_zeros(df:pd.DataFrame, columns:list) -> pd.DataFrame:
        for column in columns:
            median = df[df[column] != 0][column].median()
            df[column] = df.apply(lambda x: x[column] if x[column] != 0 else median, axis=1)
        return df

    @staticmethod
    def outliers_filter(df:pd.DataFrame, filter_columns:list, std_dev:int=2) -> pd.DataFrame:
        df_zscore = stats.zscore(df[filter_columns])
        df_std_dev = np.abs(df_zscore) < std_dev
        filter_ = (df_std_dev).all(axis=1)
        return df[filter_]
        
    @staticmethod
    def cleaning_df_by_quantiles(df:pd.DataFrame, lesser_quantile:float ,bigger_quantile:float , next_jump:int, columns:list=['name_of_column']) ->  pd.DataFrame:
        for column in columns:
            quantiles_df = Cleaning.quantiles_df(df=df, column=column, next_jump=next_jump)
            df = df[df[column] >= quantiles_df[lesser_quantile]]
            df = df[df[column] <= quantiles_df[bigger_quantile]]
        return df

    def quantiles_df(df:pd.DataFrame, column:str, next_jump:int=1) -> pd.DataFrame:
        return df[column].quantile(Cleaning._quantiles_(next_jump))

    @staticmethod
    def _quantiles_(next_jump:int=5) -> list:
        return [value/100 for value in range(0, 100 + next_jump, next_jump)]

    @staticmethod
    def generating_distribution_graf(df:pd.DataFrame, columns:list, bins:int=100) -> None:
        for column_name in columns:
            bins = len(df[column_name]) if len(df[column_name]) < bins else bins
            plt.hist(df[column_name], bins=bins ,density=True, stacked=True)

            # Add a vertical line at the mean of the z-scores
            plt.axvline(df[column_name].mean(), color='k', linestyle='dashed', linewidth=1)
            # Add vertical lines at one and two standard deviations from the mean
            plt.axvline(df[column_name].mean() + 2*df[column_name].std(), color='k', linestyle='dashed', linewidth=1)
            plt.axvline(df[column_name].mean() - 2*df[column_name].std(), color='k', linestyle='dashed', linewidth=1)

            # Add a title and labels to the axes
            plt.title(f'Distribution of {column_name}')
            plt.xlabel(f'{column_name}')
            plt.ylabel('Probability')
            plt.xlim(left=min(df[column_name]), right=max(df[column_name]))
    # Show the plot
            plt.show()

class Categorization:
    @staticmethod
    def generating_dummie_values(df:pd.DataFrame, columns_to_transform_to_dummies:list) -> pd.DataFrame:
        for column in columns_to_transform_to_dummies:
            dummies_dict = Categorization.dummies_dict(df=df, column=column)
            df[column + '_dummie_'] = df[column].apply(lambda x: dummies_dict[x])
        return df

    @staticmethod
    def dummies_dict(df:pd.DataFrame, column:str) -> list:
        return dict(zip( sorted(df[column].unique()), list(range(1, df[column].nunique()+1 )) ))