from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use DATABASE_URL if set, otherwise default to SQLite
db_url = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=1)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    tasks = Task.query.order_by(Task.priority.asc()).all()
    # Pass a list of tuples for compatibility with tasks.html
    tasks_list = [(t.id, t.task, t.priority) for t in tasks]
    return render_template('tasks.html', tasks=tasks_list)

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('task')
    priority = request.form.get('priority')
    if new_task:
        task = Task(task=new_task, priority=int(priority))
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)