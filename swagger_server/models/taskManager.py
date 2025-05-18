from swagger_server.models.new_task import NewTask
from swagger_server.models.task import Task
from typing import Dict

class TaskManager:
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self.current_id = 0


    def is_id_exist_util_func(self, task_id):
        if task_id not in self._tasks:
            raise KeyError("Task not found")

    def get_all_tasks(self):
        return self._tasks
    
    def create_new_task(self,  input_task: NewTask):
        self.current_id += 1
        new_task = Task(self.current_id, input_task.title, input_task.description, False)
        self._tasks[self.current_id] = new_task
        return new_task
    
    def delete_all_tasks(self):
        self._tasks = {}

    def delete_task(self, task_id):
        self.is_id_exist_util_func(task_id)
        self._tasks.pop(task_id)
    
    def get_task(self, task_id):
        self.is_id_exist_util_func(task_id)
        return self._tasks[task_id]
        
    def update_task(self, task_id, update: NewTask):
        self.is_id_exist_util_func(task_id)
        task_to_update = self._tasks[task_id]
        task_to_update.title = update.title
        task_to_update.description = update.description
        return task_to_update

    def set_task_complete(self, task_id):
        self.is_id_exist_util_func(task_id)
        self._tasks[task_id].completed = True
        return self._tasks[task_id]

    