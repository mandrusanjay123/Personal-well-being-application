# clustering.py

def assign_user_cluster(hours_per_day, productive_time, break_frequency, wellness_activities):
    """
    Assigns the user to a productivity cluster based on their questionnaire responses.

    Parameters:
        - hours_per_day (int): The number of hours the user can dedicate to tasks each day.
        - productive_time (str): The time of day the user feels most productive ("morning", "afternoon", or "evening").
        - break_frequency (str): The frequency of breaks the user prefers ("often", "sometimes", or "rarely").
        - wellness_activities (str): Whether the user engages in wellness activities daily ("yes" or "no").

    Returns:
        - str: The cluster name, either "morning_person", "evening_person", or "night_owl".
    """

    # Convert qualitative responses to numerical values for potential clustering (if required in the future)
    productive_time_map = {"morning": 1, "afternoon": 2, "evening": 3}
    break_frequency_map = {"often": 1, "sometimes": 2, "rarely": 3}
    wellness_map = {"yes": 1, "no": 0}

    # Create a feature vector based on user input (not used directly in this simple example)
    features = [
        hours_per_day,
        productive_time_map[productive_time],
        break_frequency_map[break_frequency],
        wellness_map[wellness_activities]
    ]

    # Simple logic for cluster assignment based on the productive time preference
    if productive_time == "morning":
        return "morning_person"
    elif productive_time == "afternoon":
        return "evening_person"
    else:  # productive_time == "evening"
        return "night_owl"
