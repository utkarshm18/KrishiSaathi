from django.urls import path
from .views import recommend_view

urlpatterns = [
    path('', recommend_view, name='recommendation_form'),
]
