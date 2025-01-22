from django.core.management.base import BaseCommand
import pandas as pd
from home.models import Crop

class Command(BaseCommand):
    help = 'Load crop data from an Excel file into the database'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\91857\Desktop\SIH Project\SIH_Project\Refined_India_Agri_Data_Hindi.xlsx'
        df = pd.read_excel(file_path)
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

        for _, row in df.iterrows():
            Crop.objects.create(
                region=row['region'],
                soil_type=row['soil_type'],
                season=row['season'],
                crop=row['crop'],
                crop_hindi=row['crop_hindi'],
                water_need=row['water_need'],
                water_need_hindi=row['water_need_hindi'],
                irrigation_schedule=row['irrigation_schedule'],
                irrigation_schedule_hindi=row['irrigation_schedule_hindi'],
                pesticide=row['pesticide'],
                pesticide_hindi=row['pesticide_hindi'],
                rainfall_water_availability=row['rainfall_water_availability']
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded crop data into the database.'))
