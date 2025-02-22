# tasks.py
from typing import Any

class Task:
    def __init__(self, task_id: str, description: str, assigned_agent: str):
        self.task_id = task_id
        self.description = description
        self.assigned_agent = assigned_agent
        self.completed = False
        self.response = None

    def mark_completed(self, response: Any):
        self.completed = True
        self.response = response

    def __repr__(self):
        return f"Task({self.task_id}, assigned to: {self.assigned_agent}, completed: {self.completed})"
