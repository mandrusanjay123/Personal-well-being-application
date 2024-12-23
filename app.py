from flask import Flask, render_template, request, redirect, url_for, flash, session
# from models.user_manager import save_user_profile, get_user_cluster
from models.user_manager import save_user_profile
from models.task_manager import save_task, generate_personalized_schedule
# from models.task_manager import save_task, get_tasks_due_today, generate_personalized_schedule
from models.db import init_db
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
init_db()  # Initialize the database on startup

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assign_cluster', methods=['POST'])
def assign_cluster():
    user_data = {
        "email": request.form.get('email'),
        "hours_per_day": int(request.form.get('hours_per_day', 0)),
        "productive_time": request.form.get('productive_time', ''),
        "break_frequency": request.form.get('break_frequency', ''),
        "wellness_activities": request.form.get('wellness_activities', ''),
    }
    user_cluster = save_user_profile(user_data)
    flash(f"You have been assigned to the '{user_cluster}' cluster.", "info")
    session['user_email'] = user_data['email']
    session['user_cluster'] = user_cluster
    return redirect(url_for('task_page'))

@app.route('/task', methods=['GET', 'POST'])
def task_page():
    if 'user_email' not in session:
        flash("Please complete the questionnaire first.", "warning")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        task = {
            "name": request.form.get('task_name'),
            "deadline": request.form.get('deadline'),
            "stress_level": int(request.form.get('stress_level', 0)),
            "category": request.form.get('category'),
            "estimated_time": int(request.form.get('estimated_time', 0))
        }
        save_task(session['user_email'], task)
        flash("Task saved successfully!", "success")
        return redirect(url_for('show_schedule'))
    
    return render_template('task_form.html')

@app.route('/schedule')
def show_schedule():
    if 'user_email' not in session:
        flash("Please complete the questionnaire first.", "warning")
        return redirect(url_for('index'))
    
    user_email = session['user_email']
    user_cluster = session.get('user_cluster', 'morning_person')
    user_profile = {"time_of_day": 8, "previous_day_energy": 50}  # Placeholder profile features

    # Generate personalized schedule
    schedule = generate_personalized_schedule(user_email, user_profile)
    return render_template('schedule.html', schedule=schedule)

@app.route('/reflect', methods=['POST'])
def reflect():
    user_email = session.get('user_email')
    feedback = request.form.get('reflection_feedback')
    # Store feedback in database or file for periodic model retraining
    
    flash("Reflection saved. Thank you for your feedback!", "success")
    return redirect(url_for('show_schedule'))

if __name__ == '__main__':
    app.run(debug=True)
