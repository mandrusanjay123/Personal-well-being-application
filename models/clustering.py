def assign_user_cluster(hours_per_day, productive_time, break_frequency, wellness_activities):
    productive_time_map = {"morning": 1, "afternoon": 2, "evening": 3}
    break_frequency_map = {"often": 1, "sometimes": 2, "rarely": 3}
    wellness_map = {"yes": 1, "no": 0}

    if productive_time == "morning":
        return "morning_person"
    elif productive_time == "afternoon":
        return "evening_person"
    else:
        return "night_owl"
