import joblib
import numpy as np
import pandas as pd
from config import TASK_PRIORITY_MODEL_PATH, ENERGY_PREDICTION_MODEL_PATH, TIME_SLOT_MATCHING_MODEL_PATH
from datetime import datetime


# Load the task prioritization, energy prediction, and time slot matching models
task_priority_model = joblib.load(TASK_PRIORITY_MODEL_PATH)
energy_prediction_model = joblib.load(ENERGY_PREDICTION_MODEL_PATH)
time_slot_matching_model = joblib.load(TIME_SLOT_MATCHING_MODEL_PATH)

def preprocess_task(task):
    """
    Preprocesses task data to ensure compatibility with the ML model.

    Parameters:
        - task (dict): Dictionary containing task attributes like 'stress_level', 'deadline', 'estimated_time', and possibly other fields.
    
    Returns:
        - pd.DataFrame: Preprocessed task data as a DataFrame.
    """
    # Convert task to a dictionary if it's a tuple
    if isinstance(task, tuple):
        task = {
            'name': task[1],          # Adjust the index based on your tuple structure
            'stress_level': task[4],   # Adjust index accordingly
            'deadline': task[5],       # Adjust index accordingly
            'estimated_time': task[6], # Adjust index accordingly
            'type': task[2]            # Assuming 'type' or category of task is at index 2
        }

    # Convert the task dictionary to a DataFrame for one-hot encoding
    task_df = pd.DataFrame([task])

    # Apply one-hot encoding to the 'type' column
    task_df = pd.get_dummies(task_df, columns=['type'], drop_first=True)

    # Add any missing columns that the model expects (for example, if task types vary)
    expected_columns = task_priority_model.named_steps['preprocessor'].get_feature_names_out()
    for col in expected_columns:
        if col not in task_df:
            task_df[col] = 0  # Set missing columns to 0

    return task_df[expected_columns]

def prioritize_task(task):
    """
    Assigns a priority score to a task using the task prioritization model.
    
    Parameters:
        - task (dict): Dictionary containing task attributes like 'stress_level', 'deadline', 'estimated_time', and 'category'.
        
    Returns:
        - float: The priority score for the task.
    """
    # Define the required columns that the model expects
    required_columns = ['stress_level', 'deadline', 'estimated_time', 'category']
    
    # Ensure all required columns are present in the task
    missing_columns = [col for col in required_columns if col not in task]
    if missing_columns:
        raise ValueError(f"Task is missing columns: {missing_columns}")
    
    # Convert deadline to numeric format (days until deadline)
    if isinstance(task['deadline'], str):
        deadline_date = datetime.strptime(task['deadline'], "%Y-%m-%d")
        days_until_deadline = (deadline_date - datetime.now()).days
        task['deadline'] = days_until_deadline
    
    # Prepare task features for the model, ensuring column consistency
    task_features = pd.DataFrame([task])[required_columns]
    
    # Debugging output to verify columns and data
    print("Task features columns:", task_features.columns)
    print("Task features data:", task_features.head())
    
    # Predict the priority score
    priority_score = task_priority_model.predict(task_features)[0]
    return priority_score


def predict_energy(user_profile, previous_energy, feedback):
    # Create a DataFrame with the correct column names expected by the model
    features = pd.DataFrame([{
        'time_of_day': user_profile['time_of_day'],
        'previous_day_energy': previous_energy,
        'schedule_feedback': feedback
    }])
    
    # Debugging output to verify the structure
    print("Energy prediction features:\n", features)
    
    # Perform the prediction
    predicted_energy = energy_prediction_model.predict(features)[0]
    return predicted_energy

def match_time_slot(task_priority, energy_level):
    """
    Matches a time slot based on task priority and energy level.
    """
    features = pd.DataFrame([[task_priority, energy_level]], columns=['task_priority', 'energy_level'])
    print("Time slot matching features:", features)
    time_slot = time_slot_matching_model.predict(features)[0]
    return time_slot

def generate_schedule(tasks, user_profile):
    """
    Generates a personalized schedule for the user based on tasks and user profile.
    
    Parameters:
        - tasks (list): List of tasks to schedule.
        - user_profile (dict): User profile attributes.
        
    Returns:
        - list: A list of scheduled tasks with time slots.
    """
    schedule = []
    
    for task in tasks:
        # Calculate task priority
        priority_score = prioritize_task(task)
        
        # Predict energy level (placeholder logic for previous energy and feedback)
        predicted_energy = predict_energy(user_profile, previous_energy=0.5, feedback=0.5)

        # Match to a time slot
        time_slot = match_time_slot(priority_score, predicted_energy)
        
        # Append to schedule
        schedule.append({
            'task': task['name'],  # Assuming task name is at index 1 in the tuple
            'priority_score': priority_score,
            'time_slot': time_slot
        })
    
    return schedule
