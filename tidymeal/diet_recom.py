# -*- coding: utf-8 -*-
import pandas as pd

dataset = pd.read_csv("static/dataset.csv")

columns=['RecipeId','Name','CookTime','PrepTime','TotalTime','RecipeIngredientParts','Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent','RecipeInstructions']
dataset=dataset[columns]

extracted_data = dataset.copy()

#nutritition values are between 6 (calories) to 14(protein content)
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
prep_data=scaler.fit_transform(extracted_data.iloc[:,6:15].to_numpy())

import joblib
from sklearn.neighbors import NearestNeighbors
loaded_model = joblib.load('static/saved_model.sav')
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

def custom_formatting(my_list):
    breakfast_list = my_list[0]
    lunch_list = my_list[1]
    dinner_list = my_list[2]

    return breakfast_list, lunch_list, dinner_list
