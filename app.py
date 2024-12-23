from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.task_storage import init_db, save_task
from models.scheduling import generate_schedule
from models.clustering import assign_user_cluster

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messaging
init_db()  # Initialize the database at startup

@app.route('/')
def index():
    return render_template('questionnaire.html')

@app.route('/assign_cluster', methods=['POST'])
def assign_cluster():
    hours_per_day = int(request.form.get('hours_per_day', 0))
    productive_time = request.form.get('productive_time', '')
    break_frequency = request.form.get('break_frequency', '')
    wellness_activities = request.form.get('wellness_activities', '')

    user_cluster = assign_user_cluster(hours_per_day, productive_time, break_frequency, wellness_activities)
    flash(f"You have been assigned to the '{user_cluster}' cluster.", "info")

    # Store user information in the session
    session['user_id'] = 1  # Use a unique user ID if available
    session['user_cluster'] = user_cluster

    return redirect(url_for('task_page'))

@app.route('/task', methods=['GET', 'POST'])
def task_page():
    user_id = session.get('user_id')
    user_cluster = session.get('user_cluster', 'morning_person')  # Default to 'morning_person'

    if request.method == 'POST':
        task_type = request.form.get('task_type')
        estimated_time = int(request.form.get('estimated_time', 0))
        stress_level = int(request.form.get('stress_level', 0))
        priority = int(request.form.get('priority', 0))
        urgency = int(request.form.get('urgency', 0))

        if not all([task_type, estimated_time, stress_level, priority, urgency]):
            flash("All fields are required.", "danger")
            return redirect(url_for('task_page'))

        save_task(user_id, task_type, estimated_time, stress_level, priority, urgency)
        flash("Task saved successfully!", "success")

        return redirect(url_for('show_schedule'))

    return render_template('task_form.html')

@app.route('/schedule')
def show_schedule():
    user_id = session.get('user_id')
    user_cluster = session.get('user_cluster', 'morning_person')  # Default to 'morning_person'

    schedule = generate_schedule(user_id, user_cluster)
    return render_template('schedule.html', schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
