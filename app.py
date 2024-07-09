from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from database_sqlalchemy import db, User, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


#  Fetches all tasks associated with the user.
@app.route('/tasks', methods=['GET'])
def fetch_tasks():
    user_email = request.headers.get('X-User-Email')
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    tasks = Task.query.filter_by(user_id=user.id).all()
    return jsonify([task.to_dict() for task in tasks])


#  Creates a new task for the user.
#  It requires the user email in the request headers and task details in the request body.
#  The task is associated with the user based on the email provided. If the user does not exist,
#  an error response is returned. If the task is created successfully, a success response is returned.
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        user_email = request.headers.get('X-User-Email')
        if not user_email:
            return jsonify({'error': 'User email is required'}), 400

        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input'}), 400

        title = data.get('title')
        if not title:
            return jsonify({'error': 'Title is required'}), 400

        description = data.get('description')
        completed = data.get('completed', False)
        due_date = data.get('due_date')

        new_task = Task(title=title, description=description, completed=completed, due_date=due_date, user_id=user.id)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task created successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Error creating task: {e}'}), 500


# Modify a single task based on the task_id provided in the URL.
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def modify_task(task_id):
    user_email = request.headers.get('X-User-Email')
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    task_data = request.json
    if not task_data or 'title' not in task_data:
        return jsonify({"error": "Task title is required"}), 400

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.title = task_data['title']
    task.description = task_data.get('description', task.description)
    task.completed = task_data.get('completed', task.completed)
    task.due_date = task_data.get('due_date', task.due_date)

    db.session.commit()
    return jsonify(task.to_dict())


# Removes a single task based on the task_id provided in the URL.
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    user_email = request.headers.get('X-User-Email')
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return '', 204


# Register a new user with the provided email.
@app.route('/register', methods=['POST'])
def register_user():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(user.to_dict()), 201

    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


# Test endpoint to check if the API is working.
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working"}), 200


if __name__ == '__main__':
    app.run(debug=True)
