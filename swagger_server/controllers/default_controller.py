from flask import jsonify, current_app, request
import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.login_body import LoginBody  # noqa: E501
from swagger_server.models.new_task import NewTask  # noqa: E501
from swagger_server.models.task import Task  # noqa: E501
from swagger_server import util
import jwt
import datetime
from functools import wraps


def generate_token(username, secret_key):
    return jwt.encode(
        {
            'username': username,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
        },
        secret_key,
        algorithm="HS256"
    )

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            token = token.split(" ")[1] if "Bearer" in token else token
            jwt.decode(token, current_app.config["FLASK_SECRET"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401

        return f(*args, **kwargs)
    return decorated

@token_required
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


def login_post(body):  # noqa: E501
    """Login to get JWT token

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = LoginBody.from_dict(connexion.request.get_json())  # noqa: E501
    return generate_token(body.username, current_app.config["FLASK_SECRET"])

@token_required
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

@token_required
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

@token_required
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

@token_required
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
