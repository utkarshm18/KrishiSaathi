# home/views.py
# home/views.py
from django.shortcuts import render
from .models import Crop

def recommend_crops(region, soil_type, season):
    water_availability_map = {'Low': 1, 'Medium': 2, 'High': 3}
    water_scores = {'Low': 1, 'Medium': 2, 'High': 3}

    def calculate_water_score(crop, water_availability):
        crop_water_need = water_scores.get(crop.water_need, 2)
        if crop_water_need == water_availability:
            return 10
        elif abs(crop_water_need - water_availability) == 1:
            return 5
        else:
            return 2

    def calculate_soil_score(crop, soil_type):
        suitable_soils = {
            'Rice': ['Loamy', 'Clayey'],
            'Wheat': ['Sandy', 'Loamy'],
            'Maize': ['Loamy', 'Sandy Loam'],
            # Add other crops as needed
        }
        match_strength = len(set([soil_type]) & set(suitable_soils.get(crop.crop, [])))
        if match_strength == 2:
            return 10
        elif match_strength == 1:
            return 5
        else:
            return 1

    def calculate_season_score(crop, season):
        if crop.season.strip().lower() == season.strip().lower():
            return 30
        else:
            return 0

    filtered_crops = Crop.objects.filter(region=region, soil_type=soil_type, season=season)
    
    recommendations = []
    for crop in filtered_crops:
        water_availability = water_availability_map.get(crop.rainfall_water_availability, 2)
        water_score = calculate_water_score(crop, water_availability)
        soil_score = calculate_soil_score(crop, soil_type)
        season_score = calculate_season_score(crop, season)

        total_crop_score = water_score + soil_score + season_score

        recommendations.append({
            'crop': crop.crop,
            'score': total_crop_score,
            'water_need': crop.water_need,
            'irrigation_schedule': crop.irrigation_schedule,
            'pesticide': crop.pesticide
        })

    recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)
    return recommendations

from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse

import logging

# Set up logging
logger = logging.getLogger(__name__)

def crop_recommendation(request):
    # Define options for dropdown menus
    regions = ['Punjab', 'Haryana', 'Uttar Pradesh', 'Maharashtra']
    soil_types = ['Loamy', 'Clayey', 'Sandy', 'Sandy Loam']
    seasons = ['Kharif', 'Rabi', 'Zaid']

    if request.method == 'POST':
        region = request.POST.get('region')
        soil_type = request.POST.get('soil_type')
        season = request.POST.get('season')

        # Log form data
        logger.debug(f"Form data received: region={region}, soil_type={soil_type}, season={season}")

        # Call the recommendation function
        recommendations = recommend_crops(region, soil_type, season)

        # Log recommendations
        logger.debug(f"Recommendations: {recommendations}")

        return render(request, 'home/crop_form.html', {
            'regions': regions,
            'soil_types': soil_types,
            'seasons': seasons,
            'selected_region': region,
            'selected_soil_type': soil_type,
            'selected_season': season,
            'recommendations': recommendations  # Pass recommendations to template
        })
    
    return render(request, 'home/crop_form.html', {
        'regions': regions,
        'soil_types': soil_types,
        'seasons': seasons
    })



def home(request):
    return render(request, 'home/home.html')

def index(request):
    return render(request, 'index.html')

def farmer_portal(request):
    return render(request, 'home/farmer.html')

def public_view(request):
    return render(request, 'home/public.html')

def sustainable(request):
    return render(request, 'sustainable.html')

def groundwater_map(request):
    return render(request, 'home/groundwater_map.html')

def farmer_page(request):
    return render(request, 'home/farmer_page.html')
def public_page(request):
    return render(request, 'public.html')
def prediction_page(request):
    return render(request, 'prediction.html')
























from django.shortcuts import render
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import os
# data = pd.read_csv(r'C:\Users\91857\Desktop\SIH Project\SIH_Project\home\combined.csv')
# data = pd.read_csv(r'D:\Desktop\SIH_Project_Final\SIH_Project\home\combined.csv')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = os.path.join(BASE_DIR, 'home', 'combined.csv')

def perform_linear_regression(state, future_year):
    # Filter data for the given state
    state_data = data[data['State Name'] == state]

    if state_data.empty:
        return {
            'error': f'No data found for state {state}.'
        }

    # Extract features and target
    X = state_data[['Year']]
    y_net_availability = state_data['Net Groundwater Availability']
    y_stage_development = state_data['Stage of Goundwater Development (%)']

    # Initialize linear regression models
    net_availability_model = LinearRegression()
    stage_development_model = LinearRegression()

    # Fit models
    net_availability_model.fit(X, y_net_availability)
    stage_development_model.fit(X, y_stage_development)

    # Predict for the specific future year
    future_net_availability = net_availability_model.predict([[future_year]])
    future_stage_development = stage_development_model.predict([[future_year]])

    return {
        'future_net_availability': future_net_availability[0],
        'future_stage_development': future_stage_development[0]
    }


def prediction(request):
    if request.method == 'POST':
        user_input_state = request.POST.get('state')
        user_input_year = int(request.POST.get('year'))
        prediction_results = perform_linear_regression(user_input_state, user_input_year)
        return render(request, 'home/prediction.html', {'prediction_results': prediction_results})
    else:
        return render(request, 'home/prediction.html')