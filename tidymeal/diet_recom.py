# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from random import uniform as rnd
import numpy as np

class MealRecommender:
    def __init__(self, dataset_path, model_path):
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.columns = [
            'RecipeId', 'Name', 'CookTime', 'PrepTime', 'TotalTime', 'RecipeIngredientParts',
            'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
            'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent', 'RecipeInstructions'
        ]
        self._load_data()
        self._load_model()
        self._setup_pipeline()
    
    def _load_data(self):
        self.dataset = pd.read_csv(self.dataset_path)
        self.extracted_data = self.dataset[self.columns].copy()
    
    def _load_model(self):
        self.loaded_model = joblib.load(self.model_path)
    
    def _setup_pipeline(self):
        self.scaler = StandardScaler()
        self.prep_data = self.scaler.fit_transform(self.extracted_data.iloc[:, 6:15].to_numpy())
        self.neigh = self.loaded_model
        transformer = FunctionTransformer(self.neigh.kneighbors, kw_args={'return_distance': False})
        self.pipeline = Pipeline([('std_scaler', self.scaler), ('NN', transformer)])
        params = {'n_neighbors': 10, 'return_distance': False}
        self.pipeline.set_params(NN__kw_args=params)
    
    def get_recommendations(self, total_calories):
        meal_list = ['breakfast', 'lunch', 'dinner']
        recommendations = []
        for meal in meal_list:
            recommended_nutrition = self._generate_nutrition(meal, total_calories)
            index = self.pipeline.transform(np.asarray(recommended_nutrition).reshape(1, -1))[0]
            list_of_recom = self.extracted_data.iloc[index]
            list_of_strings = [[row['Name'], str(row['Calories'])] for _, row in list_of_recom.iterrows()]
            recommendations.append(list_of_strings)
        return recommendations
    
    def _generate_nutrition(self, meal, total_calories):
        if meal == 'breakfast':
            return [total_calories * 0.20, rnd(0, 10), rnd(0, 4), rnd(0, 10), rnd(0, 20), rnd(0, 15), rnd(0, 10), rnd(0, 10), rnd(0, 20)]
        elif meal == 'lunch':
            return [total_calories * 0.40, rnd(20, 40), rnd(0, 4), rnd(0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 20), rnd(0, 10), rnd(50, 175)]
        elif meal == 'dinner':
            return [total_calories * 0.40, rnd(20, 40), rnd(0, 4), rnd(0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 20), rnd(0, 10), rnd(50, 175)]

def custom_formatting(my_list):
    breakfast_list = my_list[0]
    lunch_list = my_list[1]
    dinner_list = my_list[2]

    return breakfast_list, lunch_list, dinner_list
