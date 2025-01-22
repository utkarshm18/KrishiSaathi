from django.shortcuts import render
import pandas as pd

import os
from django.conf import settings

def load_data():
    # file_path = r'C:\Users\91857\Desktop\SIH Project\SIH_Project\recommender\Refined_India_Agri_Data_Hindi.xlsx'
    # file_path = r'D:\Desktop\SIH_Project_Final\SIH_Project\recommender\Refined_India_Agri_Data_Hindi.xlsx'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, 'recommender', 'Refined_India_Agri_Data_Hindi.xlsx')
    df = pd.read_excel(file_path)
    # df = pd.read_csv('home/combined.csv')
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df

def calculate_scores(df, region, soil_type, season):
    def calculate_water_score(crop, water_availability):
        water_scores = {'Low': 1, 'Medium': 2, 'High': 3}
        crop_water_score = water_scores.get(crop['water_need'], 2)

        if crop_water_score == water_availability:
            return 10
        elif abs(crop_water_score - water_availability) == 1:
            return 5
        else:
            return 2

    def calculate_soil_score(crop, soil_type):
        suitable_soils = {
            'Rice': ['Loamy', 'Clayey'],
            'Wheat': ['Sandy', 'Loamy'],
            
        }

        match_strength = len(set([soil_type]) & set(suitable_soils.get(crop['crop'], [])))
        if match_strength == 2:
            return 10
        elif match_strength == 1:
            return 5
        else:
            return 1

    def calculate_season_score(crop, season):
        if crop['season'].strip().lower() == season.strip().lower():
            return 30
        else:
            return 0

    filtered_df = df[(df['region'] == region) & (df['soil_type'] == soil_type) & (df['season'] == season)]

    recommendations = []
    water_availability_map = {'Low': 1, 'Medium': 2, 'High': 3}

    for _, crop in filtered_df.iterrows():
        water_availability = water_availability_map.get(crop['rainfall_water_availability'], 2)
        water_score = calculate_water_score(crop, water_availability)
        soil_score = calculate_soil_score(crop, soil_type)
        season_score = calculate_season_score(crop, season)

        total_crop_score = water_score + soil_score + season_score

        recommendations.append({
            'crop': crop['crop'],
            'score': total_crop_score,
            'water_need': crop['water_need'],
            'irrigation_schedule': crop['irrigation_schedule'],
            'pesticide': crop['pesticide']
        })

    return sorted(recommendations, key=lambda x: x['score'], reverse=True)

def recommend_view(request):
    df = load_data()
    if request.method == 'POST':
        region = request.POST['region']
        soil_type = request.POST['soil_type']
        season = request.POST['season']

        recommendations = calculate_scores(df, region, soil_type, season)

        return render(request, 'recommender/results.html', {'recommendations': recommendations})

    return render(request, 'recommender/form.html')

def recommend_view(request):
    # Load data and handle form submissions here
    return render(request, 'recommender/form.html')
