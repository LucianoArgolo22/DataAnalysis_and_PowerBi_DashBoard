#%%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Clients.ClientProcessingCleaning import Categorization
from scipy import stats

"""
from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(categorical_features=[0])
ohe.fit_transform(X).toarray()
"""

cwd = '/'.join(__file__.split('/')[:-2])
df = pd.read_csv(f'{cwd}/utils/data/dataset_filtrado.csv')

df = df[['price','meters','rooms','subzone1','Date']]
df = df[df['rooms'] < 6]
#%%
#SI QUIERO COMPARAR UN BARRIO CONTRA OTRO EN EL SCATTER SIRVE REDUCIR EL DATASET
#df = df[(df.subzone1 == 'Constitucion') | (df.subzone1 == 'Las Cañitas')]
#%%
df.groupby('subzone1').count()
#%%
"""from sklearn.preprocessing import OneHotEncoder

#creating instance of one-hot-encoder
encoder = OneHotEncoder(handle_unknown='ignore')

#perform one-hot encoding on 'team' column 
encoder_df = pd.DataFrame(encoder.fit_transform(df[['subzone1']]).toarray())

#merge one-hot encoded columns back with original DataFrame
final_df = df.join(encoder_df)

#view final df
final_df2 = final_df.groupby('subzone1').agg([np.mean])
"""
#%%

df = Categorization.generating_dummie_values(df=df, columns_to_transform_to_dummies=['subzone1'])

#%%
sns.scatterplot(x ="price", y ="meters", data = df)
#%%
#comparación de barrios
sns.lmplot(x ="price", y ="meters", data = df, hue='subzone1', order= 1)
#%%
sns.lmplot(x ="price", y ="meters", data = df, hue='rooms', order= 2)

# %%
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







#%%
"""
#%%
#transforming the shape of the data to put into de the train_test method
X = np.array(df['price']).reshape(-1, 1)
Y = np.array(df['meters']).reshape(-1, 1)
# %%
#generating the outputs of the train model
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.20)
# %%
#creating the LinearRegression object
regr = LinearRegression()
# %%
#fitting the model
regr.fit(X_train, y_train)
print(regr.score(X_test, y_test))


#%%
#plotting the Scatter plot to check relationship between Sal and Temp
sns.lmplot(x ="meters", y ="price", data = df_binary, order = 2, ci = None)

X = np.array(df_binary['price']).reshape(-1, 1)
Y = np.array(df_binary['meters']).reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.25)

regr =  LinearRegression()

regr.fit(X_train, y_train)
print(regr.score(X_test, y_test))


#%%
y_pred = regr.predict(X_test)
plt.scatter(X_test, y_test, color ='b')
plt.plot(X_test, y_pred, color ='k')
  
plt.show()
"""