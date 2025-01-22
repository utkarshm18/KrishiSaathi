from django.db import models

class CropRecommendation(models.Model):
    region = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    crop = models.CharField(max_length=100)
    crop_hindi = models.CharField(max_length=100)
    water_need = models.CharField(max_length=100)
    water_need_hindi = models.CharField(max_length=100)
    irrigation_schedule = models.CharField(max_length=200)
    irrigation_schedule_hindi = models.CharField(max_length=200)
    pesticide = models.CharField(max_length=100)
    pesticide_hindi = models.CharField(max_length=100)
    rainfall_water_availability = models.CharField(max_length=100, default="Unknown")
  # New field

    def __str__(self):
        return f"{self.crop} ({self.season}) in {self.region}"
    
class ReservoirPrediction(models.Model):
    reservoir_name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=50)
    mean_absolute_error = models.FloatField()
    mean_squared_error = models.FloatField()
    r2_score = models.FloatField()
    cross_validated_mae = models.FloatField()
    model_file = models.CharField(max_length=255)

# home/models.py
from django.db import models

from django.db import models

class Crop(models.Model):
    region = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    crop = models.CharField(max_length=100)
    crop_hindi = models.CharField(max_length=255, null=True, blank=True)
    water_need = models.CharField(max_length=50)
    water_need_hindi = models.CharField(max_length=50)
    irrigation_schedule = models.CharField(max_length=255)
    irrigation_schedule_hindi = models.CharField(max_length=255)
    pesticide = models.CharField(max_length=255)
    pesticide_hindi = models.CharField(max_length=255)
    rainfall_water_availability = models.CharField(max_length=50)

    def __str__(self):
        return self.crop

