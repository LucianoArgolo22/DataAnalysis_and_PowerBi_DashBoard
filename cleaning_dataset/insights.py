#%%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Clients.ClientProcessingCleaning import Categorization
from scipy import stats



cwd = '/'.join(__file__.split('/')[:-2])
df = pd.read_csv(f'{cwd}/utils/data/dataset_filtrado.csv')

df = df[['price','meters','rooms','subzone1','Date']]
df = df[df['rooms'] < 6]

df.groupby('subzone1').count()


df = Categorization.generating_dummie_values(df=df, columns_to_transform_to_dummies=['subzone1'])

sns.scatterplot(x ="price", y ="meters", data = df)

sns.lmplot(x ="price", y ="meters", data = df, hue='subzone1', order= 1)

sns.lmplot(x ="price", y ="meters", data = df, hue='rooms', order= 2)


#Pearson's correlation
stats.pearsonr(df['price'], df['subzone1_dummie_'])
#%%%
#
# Correlation between different variables
#
corr = df.corr()
#
# Set up the matplotlib plot configuration
#
plt.subplots(figsize=(12, 10))
#
# Configure a custom diverging colormap
#
cmap = sns.diverging_palette(230, 20)
#
# Draw the heatmap
#
sns.heatmap(corr, annot=True, cmap=cmap)
