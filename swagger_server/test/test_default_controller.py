# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.login_body import LoginBody  # noqa: E501
from swagger_server.models.new_task import NewTask  # noqa: E501
from swagger_server.models.task import Task  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_task_by_id(self):
        """Test case for get_task_by_id

        Get a specific task
        """
        response = self.client.open(
            '/tasks/{task_id}'.format(task_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_tasks(self):
        """Test case for get_tasks

        Get all tasks
        """
        response = self.client.open(
            '/tasks',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_post(self):
        """Test case for login_post

        Login to get JWT token
        """
        body = LoginBody()
        response = self.client.open(
            '/login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tasks_post(self):
        """Test case for tasks_post

        Create a new task
        """
        body = NewTask()
        response = self.client.open(
            '/tasks',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tasks_task_id_complete_get(self):
        """Test case for tasks_task_id_complete_get

        Mark a task as complete
        """
        response = self.client.open(
            '/tasks/{task_id}/complete'.format(task_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tasks_task_id_delete(self):
        """Test case for tasks_task_id_delete

        Delete a task
        """
        response = self.client.open(
            '/tasks/{task_id}'.format(task_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tasks_task_id_put(self):
        """Test case for tasks_task_id_put

        Update a task
        """
        body = NewTask()
        response = self.client.open(
            '/tasks/{task_id}'.format(task_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
