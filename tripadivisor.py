# -*- coding: utf-8 -*-
"""tripadivisor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16msJjlgg9d3iO8nc1v1e3Fqc9MTMLBem
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_excel('tripadvisor.xls')

df

df.isna().sum()

duplicate=df[df.duplicated(subset=['name','address','Phone'],keep=False)]
print(duplicate)

df.drop(['Phone','price_range_from','price_range_to'],axis=1,inplace=True)

df.cuisines.unique()

df.dropna(how='any',inplace=True)

df.info()

#excellent_count and #vgood_count has datatype object but values in numeric we have to change the datatype

df['excellent_count']=df['excellent_count'].str.replace(',','').astype(int)

df['very_good_count']=df['very_good_count'].str.replace(',','').astype(int)

df.info()

from textwrap import wrap

data=df[:10][['name','rating','review_count','excellent_count','very_good_count','average_count','poor_count','terrible_count']]
data

names=data.iloc[:,0]
barrating=data.iloc[:,1]
barreview=data.iloc[:,2]
barexcellent=data.iloc[:,3]
barvgood=data.iloc[:,4]
baravg=data.iloc[:,5]
barpoor=data.iloc[:,6]
barteri=data.iloc[:,7]
index=np.arange(len(data))

plt.figure(figsize=(20,10))
graphexcellent=plt.bar(x=index,height=barexcellent,width=0.35)
graphvgood=plt.bar(x=index,height=barvgood,width=0.35,bottom=barexcellent)
graphavg=plt.bar(x=index,height=baravg,width=0.35,bottom=barexcellent+barvgood)
graphpoor=plt.bar(x=index,height=barpoor,width=0.35,bottom=barexcellent+barvgood+baravg)
graphteri=plt.bar(x=index,height=barteri,width=0.35,bottom=barexcellent+barvgood+baravg+barpoor)
plt.legend(['Excellent','Very good','Avg','Poor','Terrible'])
plt.xlabel('Name')
plt.ylabel('Count')
names=["\n".join(wrap(name,15))for name in names]
plt.xticks(index,names)
plt.title('Review of Mumbai Restaurants')

df.cuisines.unique()

dummies = df['cuisines'].str.get_dummies(sep=', ')
df_cuisines = pd.concat([df, dummies], axis=1)
df_cuisines = df_cuisines.drop(['Bar', 'Barbecue', 'Brew Pub', 'Cafe', 'Contemporary', 'Deli', 'Diner', 'Dining bars', 'Fast food', 'Fusion', 'Gastropub', 'Gluten Free Options', 'Grill', 'Healthy', 'Pub', 'Seafood', 'Soups', 'Sports bars', 'Steakhouse', 'Street Food', 'Vegan Options', 'Vegetarian Friendly', 'Wine Bar', 'International'], axis=1)

merge_cuisines = df_cuisines['American'] + df_cuisines['Central American'] + df_cuisines['Cajun & Creole'] + df_cuisines['Southwestern']
df_cuisines['American1'] = merge_cuisines
df_cuisines['American1'] = df_cuisines.American1.replace((4, 3, 2), 1)

merge_cuisines = df_cuisines['Central-Italian'] + df_cuisines['Italian'] + df_cuisines['Northern-Italian'] + df_cuisines['Pizza'] + df_cuisines['Southern-Italian']
df_cuisines['Italian1'] = merge_cuisines
df_cuisines['Italian1'] = df_cuisines.Italian1.replace((3,2), 1)

merge_cuisines = df_cuisines['Japanese'] + df_cuisines['Sushi']
df_cuisines['Japanese1'] = merge_cuisines
df_cuisines['Japanese1'] = df_cuisines.Japanese1.replace(2, 1)

merge_cuisines = df_cuisines['Central European'] + df_cuisines['European']
df_cuisines['European1'] = merge_cuisines
df_cuisines['European1'] = df_cuisines.European1.replace(2, 1)


df_cuisines = df_cuisines.drop(['American', 'Central American', 'Cajun & Creole', 'Southwestern', 'Central-Italian', 'Italian', 'Northern-Italian', 'Pizza', 'Southern-Italian', 'Japanese', 'Sushi', 'Asian', 'Central Asian', 'Central European', 'European'], axis=1)
df_cuisines = df_cuisines.rename(columns = {'American1': 'American', 'Italian1': 'Italian', 'Japanese1': 'Japanese', 'European1': 'European'})

rest = df[['rating','name', 'review_count']]
rest_top = pd.concat([rest], ignore_index = True).dropna()
rest_top = rest_top.sort_values(by=['rating', 'review_count'], ascending = False)
rest_5 = rest_top.groupby(['rating']).get_group(5.0)
rest_4half = rest_top.groupby(['rating']).get_group(4.5)
rest_4 = rest_top.groupby(['rating']).get_group(4.0)
rest_3half = rest_top.groupby(['rating']).get_group(3.5)

import plotly.express as px

fig = px.bar(rest_5[0:10],
             x='name',
             y='review_count',
             labels={"review_count": "Highest rating based on review count",
                     "name": "Restaurant Name"},
             title = 'Top 10 5 star Restaurants in Mumbai.')
fig.show()

rest_top_review = rest_top.sort_values(by=['review_count'], ascending = False)
fig = px.bar(rest_top_review[0:10],
             x='name',
             y='review_count',
             labels={"review_count": "Review Count",
                     "name": "Restaurant Name"},
             title = 'Top 10 highest reviewed Restaurants in Mumbai')
fig.show()

df_cuisine_count = df_cuisines.drop(['name','address','cuisines','rating','review_count','excellent_count','very_good_count','average_count','poor_count','terrible_count'], axis=1)
df_cuisine_count = df_cuisine_count.sum().sort_values(ascending = False)
df_cuisine_count = df_cuisine_count.reset_index()
df_cuisine_count.columns = ['Cuisine', 'Count']

fig = px.bar(df_cuisine_count[0:10],
             x='Cuisine',
             y='Count',
             title = 'Top 10 cuisine in Mumbai')
fig.show()

rest_cuis = df_cuisines[['rating','name', 'review_count', 'Indian', 'Chinese', 'Italian', 'European', 'Thai', 'American', 'Mexican', 'Mediterranean', 'Middle Eastern', 'Japanese',]]
rest_cuis = pd.concat([rest_cuis], ignore_index = True)
rest_cuis = rest_cuis.sort_values(by=['review_count', 'rating'], ascending = False)
indian = rest_cuis.groupby(['Indian']).get_group(1.0)
chinese = rest_cuis.groupby(['Chinese']).get_group(1.0)
italian = rest_cuis.groupby(['Italian']).get_group(1.0)
european = rest_cuis.groupby(['European']).get_group(1.0)
thai = rest_cuis.groupby(['Thai']).get_group(1.0)
american = rest_cuis.groupby(['American']).get_group(1.0)
mexican = rest_cuis.groupby(['Mexican']).get_group(1.0)
mediterranean = rest_cuis.groupby(['Mediterranean']).get_group(1.0)
middle_eastern = rest_cuis.groupby(['Middle Eastern']).get_group(1.0)
japanese = rest_cuis.groupby(['Japanese']).get_group(1.0)

fig = px.bar(italian[0:10],
             x='name',
             y='review_count',
             labels={"review_count": "Highest rating based on review count",
                     "name": "Restaurant Name"},
             title = 'Top 10 Italian Restaurants in Mumbai')
fig.show()

