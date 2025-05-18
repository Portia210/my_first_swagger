#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.models.taskManager import TaskManager  

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.app.config["TASK_MANAGER"] = TaskManager()
    app.app.config["FLASK_SECRET"] = "f8b08f16ecf1e05e6d9c07e45e0378b9d6b482d4f7edb5fc64f1a9c8a1d4b4b2"
    app.add_api('swagger.yaml', arguments={'title': 'Task Management API'}, pythonic_params=True)
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    main()
