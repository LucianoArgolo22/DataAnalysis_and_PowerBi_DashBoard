#%%
import sys
sys.path.append("..") 
from Clients.ClientProcessingCleaning import Processing, Cleaning, pd

class ServiceProcessing:
    @staticmethod
    def process_columns(df:pd.DataFrame, config_json:dict) -> pd.DataFrame:
        processor = Processing(df=df)
        for config in config_json['processing_config_1']:
            processor.cleaning_columns(values=config)
        processor.df.Fix_zone = processor.df.Fix_zone.apply(lambda x: x.title())
        processor.segregating_by_fields(columns_to_segregate=config_json['columns_to_segregate'])
        processor.punctual_process(column='rooms')

        for config in config_json['processing_config_2']:
            processor.df = processor.df.dropna()
            processor.cleaning_columns(values=config)
            processor.filtering_columns_by_regex(values=config)
            processor.df = processor.df.astype({config[0]:int})
        
        for values in config_json['values_to_unify']:
            for column, values_to_be_found in values.items():
                processor.changing_values_with_tildes(column=column)
                processor.combining_similar_values_df(column=column, to_find_values=values_to_be_found)    
        return processor.df




class AutoCleaning:
    @staticmethod
    def whole_cleaning(log:object, load_path:str, save_path:str=None) -> None:
        if not load_path:
            load_path = '/'.join(__file__.split('/')[:-2])
        df = pd.read_csv(f'{load_path}\\Derpatamentos_data_set_20231.csv')
        df2 = pd.read_csv(f'{load_path}\\Derpatamentos_data_set_202212.csv')
        df = pd.concat([df,df2])
        log.info(f'Initial length of df: {len(df)}')
        df = df[['price','meters','rooms','Fix_zone','Fix_place_type','Fix_operation','currency','Date','subzone1', 'subzone2', 'subzone3', 'Urls']]

        config_json = {
            'columns_to_segregate':{ 
                                    'currency':'$',
                                    'Fix_zone':'Bsas Gba Norte',
                                    'Fix_operation':'alquiler'
                                    },
            'processing_config_1': [{'subzone2':'^\s|[.]+|\s+$', 'replace': ''}, {'subzone1':'^\s|[.]+|\s+$', 'replace': ''}, {'Fix_zone':'[-]+', 'replace': ' '}, {'Fix_zone':'^\s', 'replace': ''}],
            'processing_config_2': [('price','\D+'), ('meters','\D+'), ('rooms','\D+')],
            'values_to_unify': [{'subzone1': ['Boca', 'Belgrano', 'Almagro', 'Caballito', 'Floresta', 'Palermo', 'Mitre', 'Santa Rita', 'Nuñez', 'Urquiza', 'Pompeya']}, {'Fix_place_type': ['departamento', 'casa', 'terreno']}]
        }

        df = df.drop_duplicates(subset=['Urls'], keep='last')
        log.info(f'Lenght of df after dropping duplicates: {len(df)}')
        df = df[df['subzone1'].str.contains('\\d+') == False]
        print(len(df))

        df = ServiceProcessing.process_columns(df=df, config_json=config_json)
        df = df[['price', 'meters', 'rooms', 'Fix_zone', 'Fix_place_type','Fix_operation','currency','subzone1','subzone2','subzone3','Date','Urls']]

        df = df.drop_duplicates(subset=['price', 'meters', 'rooms', 'Fix_zone', 'Fix_place_type','Fix_operation','currency','subzone1','subzone2'], keep='last')
        df = df.drop_duplicates(subset=['Urls'], keep='last')
        #df = Cleaning.generating_median_for_zeros(df=df, columns=['rooms','meters'])

        df_grouped_count = df.groupby('subzone1').count()
        bigger_than_x_quantity = df_grouped_count[df_grouped_count['price'] > 10].reset_index()['subzone1']
        df = df[df['subzone1'].isin(bigger_than_x_quantity)]

        df_filtered = Cleaning.outliers_filter(df=df, filter_columns=['price','meters'])
        df_filtered = Cleaning.cleaning_df_by_quantiles(df=df_filtered, next_jump=1, lesser_quantile=0.02, bigger_quantile=0.99 ,columns=['rooms'])
        df_filtered = Cleaning.cleaning_df_by_quantiles(df=df_filtered, next_jump=1, lesser_quantile=0.07, bigger_quantile=0.93 ,columns=['meters'])
        df_filtered = Cleaning.cleaning_df_by_quantiles(df=df_filtered, next_jump=1, lesser_quantile=0.01, bigger_quantile=0.99 ,columns=['price'])
        log.info(f'Length of final data {len(df)}')
        df_filtered.to_csv(f'{save_path}\\dataset_filtrado.csv', index=False)
        


