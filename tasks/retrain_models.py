# retrain_models.py
import pandas as pd
from train_models import train_task_priority_model, train_energy_prediction_model, train_time_slot_matching_model

def retrain_models():
    feedback_data = pd.read_csv('feedback_data.csv')  # Collected feedback data
    
    # Retrain each model with updated data
    train_task_priority_model(data_path='task_data.csv')
    train_energy_prediction_model(data_path='energy_data.csv')
    train_time_slot_matching_model(data_path='time_slot_data.csv')

# Schedule this script to run weekly using a cron job or Celery task scheduler
