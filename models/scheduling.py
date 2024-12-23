import joblib
import numpy as np
from models.task_storage import get_tasks

model = joblib.load('task_scheduler_model.pkl')
scaler = joblib.load('scaler.pkl')

TIME_SLOT_MAPPING = {
    'morning_person': {0: 'morning', 1: 'afternoon', 2: 'evening'},
    'evening_person': {0: 'afternoon', 1: 'evening', 2: 'morning'},
    'night_owl': {0: 'evening', 1: 'morning', 2: 'afternoon'}
}

def predict_time_slot(task, user_cluster):
    task_features = np.array([[task[4], task[5], task[3], task[6]]])
    scaled_features = scaler.transform(task_features)
    cluster = model.predict(scaled_features)[0]
    return TIME_SLOT_MAPPING[user_cluster][cluster]

def generate_schedule(user_id, user_cluster):
    tasks = get_tasks(user_id)
    schedule = [(task, predict_time_slot(task, user_cluster)) for task in tasks]
    return schedule
