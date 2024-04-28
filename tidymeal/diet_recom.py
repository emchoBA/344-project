# -*- coding: utf-8 -*-
import pandas as pd

dataset = pd.read_csv("dataset.csv")

columns=['RecipeId','Name','CookTime','PrepTime','TotalTime','RecipeIngredientParts','Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent','RecipeInstructions']
dataset=dataset[columns]

max_Calories=2000
max_daily_fat=100
max_daily_Saturatedfat=13
max_daily_Cholesterol=300
max_daily_Sodium=2300
max_daily_Carbohydrate=325
max_daily_Fiber=40
max_daily_Sugar=40
max_daily_Protein=200 
max_list=[max_Calories,max_daily_fat,max_daily_Saturatedfat,max_daily_Cholesterol,max_daily_Sodium,max_daily_Carbohydrate,max_daily_Fiber,max_daily_Sugar,max_daily_Protein]

extracted_data=dataset.copy()
for column,maximum in zip(extracted_data.columns[6:15],max_list):
    extracted_data=extracted_data[extracted_data[column]<maximum]

#nutritition values are between 6 (calories) to 14(protein content)
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
prep_data=scaler.fit_transform(extracted_data.iloc[:,6:15].to_numpy())

import joblib
from sklearn.neighbors import NearestNeighbors
loaded_model = joblib.load('saved_model.sav')
neigh = loaded_model

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
transformer = FunctionTransformer(neigh.kneighbors,kw_args={'return_distance':False})
pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
params={'n_neighbors':10,'return_distance':False}
pipeline.get_params()
pipeline.set_params(NN__kw_args=params)

from random import uniform as rnd
import numpy

def get_recommendations(total_calories):
  meal_list = ['breakfast','launch','dinner']
  recommendations = []
  for meal in meal_list:
    if meal=='breakfast':
                recommended_nutrition = [total_calories*0.20,rnd(0,10),rnd(0,4),rnd(0,10),rnd(0,20),rnd(0,15),rnd(0,10),rnd(0,10),rnd(0,20)]
    elif meal=='launch':
                recommended_nutrition = [total_calories*0.40,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
    elif meal=='dinner':
                recommended_nutrition = [total_calories*0.40,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
    index = pipeline.transform(numpy.asarray(recommended_nutrition).reshape(1, -1))[0]

    list_of_recom = extracted_data.iloc[index]
    list_of_strings = []
    for index, row in list_of_recom.iterrows():
      row_of_strings = row.tolist()
       list_of_strings.append([row_of_strings[1],str(row_of_strings[6])])
    recommendations.append(list_of_strings)
  return recommendations

print(get_recommendations(max_Calories))
