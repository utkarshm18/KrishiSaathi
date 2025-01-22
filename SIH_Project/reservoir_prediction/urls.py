from django.urls import path
from .views import reservoir_prediction_view

urlpatterns = [
    path('predict/', reservoir_prediction_view, name='reservoir_prediction'),
]
