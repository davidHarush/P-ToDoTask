from flask import Flask, request, jsonify

from database import init_db, get_tasks, add_task, update_task, delete_task, get_user_by_email, add_user

app = Flask(__name__)

init_db()


@app.route('/tasks', methods=['GET'])
def fetch_tasks():
    user_email = request.headers.get('X-User-Email')
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    user = get_user_by_email(user_email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    tasks = get_tasks(user[0])
    return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def create_task():
    user_email = request.headers.get('X-User-Email')
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    user = get_user_by_email(user_email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = request.json
    if not task or 'title' not in task:
        return jsonify({"error": "Task title is required"}), 400

    task_id = add_task(task, user[0])
    return jsonify({"id": task_id, **task}), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def modify_task(task_id):
    user_email = request.headers.get('X-User-Email')
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    user = get_user_by_email(user_email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = request.json
    if not task or 'title' not in task:
        return jsonify({"error": "Task title is required"}), 400

    update_task(task_id, task, user[0])
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    user_email = request.headers.get('X-User-Email')
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    user = get_user_by_email(user_email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    delete_task(task_id, user[0])
    return '', 204


@app.route('/register', methods=['POST'])
def register_user():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = get_user_by_email(email)
    if user:
        user_id, user_email = user  # Unpack the tuple
        print(f'User already exists: {user_id}, {user_email}')
        return jsonify({"id": user_id, "email": user_email}), 201

    user_id = add_user(email)
    print("User created")
    print(user_id, email)
    return jsonify({"id": user_id, "email": email}), 201


if __name__ == '__main__':
    app.run(debug=True)
