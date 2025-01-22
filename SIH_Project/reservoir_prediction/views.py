import pandas as pd
from django.shortcuts import render
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

def train_and_predict_for_reservoir(reservoir_name, model_type='Random Forest', adjustment_per_year=0):
    data_path = os.path.join('reservoir_prediction', 'data', 'FINAL_RESER.xlsx')
    data = pd.read_excel(data_path)
    data = data.dropna()

    filtered_data = data[data['Reservoir_name'] == reservoir_name]
    
    if filtered_data.shape[0] < 10:
        return None, f"Not enough data for {reservoir_name}."

    X = filtered_data[['Year', 'Month', 'Full_reservoir_level', 'Live_capacity_FRL', 'Storage']]
    y = filtered_data['Level']
    
    categorical_features = ['Month']
    numerical_features = ['Year', 'Full_reservoir_level', 'Live_capacity_FRL', 'Storage']
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    model = RandomForestRegressor(random_state=42)
    
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('model', model)])
    pipeline.fit(X, y)
    
    y_pred = pipeline.predict(X)
    
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='neg_mean_absolute_error')
    
    model_filename = f'{reservoir_name}_{model_type}_level_predictor.pkl'
    joblib.dump(pipeline, model_filename)
    
    future_years = [2025, 2026, 2027, 2028, 2029]
    future_data = pd.DataFrame({
        'Year': future_years,
        'Month': [8] * len(future_years),
        'Full_reservoir_level': [50] * len(future_years),
        'Live_capacity_FRL': [30] * len(future_years),
        'Storage': [20] * len(future_years)
    })
    
    future_predictions = pipeline.predict(future_data)
    future_predictions = [pred + i * adjustment_per_year for i, pred in enumerate(future_predictions)]
    
    future_data['Predicted_Level'] = future_predictions
    
    return future_data, f"Model saved as '{model_filename}'"

from django.shortcuts import render
from .forms import ReservoirForm
from .reservoir_model import train_and_predict_for_reservoir

def reservoir_prediction_view(request):
    if request.method == 'POST':
        form = ReservoirForm(request.POST)
        if form.is_valid():
            selected_reservoir = form.cleaned_data['reservoir']
            prediction_data, message = train_and_predict_for_reservoir(
                selected_reservoir, model_type='Random Forest', adjustment_per_year=0.5
            )
            
            if prediction_data is not None:
                return render(request, 'results.html', {
                    'reservoir': selected_reservoir,
                    'data': prediction_data.to_html(index=False),  # Convert the DataFrame to HTML
                    'message': message
                })
            else:
                return render(request, 'results.html', {
                    'reservoir': selected_reservoir,
                    'message': message
                })
    else:
        form = ReservoirForm()
    
    return render(request, 'reservoir_form.html', {'form': form})

