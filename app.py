from flask import Flask, request, jsonify
from database import init_db, get_tasks, add_task, update_task, delete_task

app = Flask(__name__)

init_db()


@app.route('/tasks', methods=['GET'])
def fetch_tasks():
    """
    Endpoint to get the list of all tasks.
    """
    tasks = get_tasks()
    return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Endpoint to add a new task.
    The new task data is expected to be in JSON format in the request body.
    """
    task = request.json
    task_id = add_task(task)
    return jsonify({"id": task_id, **task}), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def modify_task(task_id):
    """
    Endpoint to update an existing task.
    The updated task data is expected to be in JSON format in the request body.
    """
    task = request.json
    update_task(task_id, task)
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    """
    Endpoint to delete an existing task by its ID.
    """
    delete_task(task_id)
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
