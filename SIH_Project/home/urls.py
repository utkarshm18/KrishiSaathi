# home/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('crop-recommendation/', views.crop_recommendation, name='crop_recommendation'),
    
    path('public/', views.public_view, name='public'),
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('farmer/', views.farmer_portal, name='farmer_portal'),
    path('home/public/', views.public_view, name='public'),
    path('sustainable/', views.sustainable, name='sustainable'),
    path('groundwater-map/', views.groundwater_map, name='groundwater_map'),
    path('farmer/', views.farmer_page, name='farmer_page'),
    path('public/', views.public_page, name='public_page'),
    path('prediction/', views.prediction, name='prediction'),
    path('prediction/', views.prediction_page, name='prediction_page'),
]
