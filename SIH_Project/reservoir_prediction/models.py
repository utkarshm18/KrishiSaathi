from django.db import models

# Create your models here.

class ReservoirPrediction(models.Model):
    reservoir_name = models.CharField(max_length=200)
    year = models.IntegerField()
    month = models.IntegerField()
    full_reservoir_level = models.FloatField()
    live_capacity_frl = models.FloatField()
    storage = models.FloatField()
    predicted_level = models.FloatField()

    def __str__(self):
        return f'{self.reservoir_name} - {self.year}/{self.month}'