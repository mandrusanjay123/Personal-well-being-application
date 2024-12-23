# scheduling.py

from models.task_storage import get_tasks

def prioritize_tasks(tasks):
    # Sort tasks based on priority (higher value indicates more priority) and urgency
    tasks = sorted(tasks, key=lambda x: (x[5], x[6]), reverse=True)
    return tasks

def cluster_based_scheduling(user_cluster, prioritized_tasks):
    # Schedule based on user cluster type
    schedule = []
    if user_cluster == 'morning_person':
        schedule = [(task, 'morning') for task in prioritized_tasks]
    elif user_cluster == 'evening_person':
        schedule = [(task, 'afternoon') for task in prioritized_tasks]
    else:  # night owl
        schedule = [(task, 'evening') for task in prioritized_tasks]
    return schedule

def generate_schedule(user_id, user_cluster):
    # Retrieve tasks specific to the user
    tasks = get_tasks(user_id)
    prioritized_tasks = prioritize_tasks(tasks)
    return cluster_based_scheduling(user_cluster, prioritized_tasks)
