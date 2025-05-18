from flask import jsonify, current_app
import connexion
from swagger_server.models.new_task import NewTask  




def get_task_by_id(task_id):  # noqa: E501
    """Get a specific task

    Retrieve a specific task by its ID # noqa: E501

    :param task_id: 
    :type task_id: int

    :rtype: Task
    """
    try:
        return current_app.config["TASK_MANAGER"].get_task(task_id)
    except KeyError as e:
        return jsonify({"error": str(e)}), 404


def get_tasks():  # noqa: E501
    """Get all tasks

    Retrieve a list of all tasks # noqa: E501


    :rtype: Dict[str, Task]
    """
    return jsonify(current_app.config["TASK_MANAGER"].get_all_tasks())


def tasks_post(body):  # noqa: E501
    """Create a new task

    Add a new task with title and description # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Task
    """
    try:
        if connexion.request.is_json:
            body = NewTask.from_dict(connexion.request.get_json())  # noqa: E501
            return jsonify(current_app.config["TASK_MANAGER"].create_new_task(body)), 201
        else:
            raise Exception
    except Exception as e:
        return jsonify({"error": str(e)}), 404


def tasks_task_id_complete_get(task_id):  # noqa: E501
    """Mark a task as complete

    Mark a specific task as completed # noqa: E501

    :param task_id: 
    :type task_id: int

    :rtype: Task
    """
    try:
        current_app.config["TASK_MANAGER"].get_task(task_id)
        completed_task = current_app.config["TASK_MANAGER"].set_task_complete(task_id)
        return jsonify(completed_task), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 404


def tasks_task_id_delete(task_id):  # noqa: E501
    """Delete a task

    Delete a specific task by ID # noqa: E501

    :param task_id: 
    :type task_id: int

    :rtype: None
    """
    try:
        current_app.config["TASK_MANAGER"].get_task(task_id)
        current_app.config["TASK_MANAGER"].delete_task(task_id)
        return jsonify({"message": "task deleted succssfully"}), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 404


def tasks_task_id_put(body, task_id):  # noqa: E501
    """Update a task

    Update a specific task by ID # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param task_id: 
    :type task_id: int

    :rtype: Task
    """
    try:
        if connexion.request.is_json:
            body = NewTask.from_dict(connexion.request.get_json())  # noqa: E501
            return jsonify(current_app.config["TASK_MANAGER"].update_task(task_id, body)), 201
        else:
            raise Exception
    except Exception as e:
        return jsonify({"error": str(e)}), 404
