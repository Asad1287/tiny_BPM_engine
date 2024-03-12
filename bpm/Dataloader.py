import json 
from bpm.ProcessDefinition import ProcessDefinition
from bpm.Task import Task
from typing import List, Optional, Any, Dict
class DataLoader:
    def __init__(self, process_file, stakeholder_file):
        self.process_file = process_file
        self.stakeholder_file = stakeholder_file

    def load_data(self):
        with open(self.process_file) as file:
            process_data = json.load(file)
        with open(self.stakeholder_file) as file:
            stakeholders = json.load(file)

        tasks = self.create_tasks(process_data)
        process_code = process_data["process_code"]
        process_name = process_data["process_name"]
        process_description = process_data["process_description"]

        process_definition = ProcessDefinition(
            process_code, process_name, process_description, tasks, stakeholders
        )

        return process_definition

    def create_tasks(self, process_data):
        tasks = []
        for task_data in process_data["tasks"]:
            options = None
            if isinstance(task_data, dict):
                task_id = task_data["task_id"]
                task_name = task_data["task_name"]
                task_type = task_data["task_type"]
                stakeholder = task_data.get("stakeholder")
                options = None
                if task_data.get("task_type") == "choice":
                    options = [
                        Task(
                            option["task_id"],
                            option["task_name"],
                            option["task_type"],
                            stakeholder=option.get("stakeholder"),
                        )
                        for option in task_data.get("options", [])
                    ]
                task = Task(
                    task_data["task_id"],
                    task_data["task_name"],
                    task_data["task_type"],
                    stakeholder=task_data.get("stakeholder"),
                    options=options,
                )
                tasks.append(task)
            else:
                task = Task(task_data, task_data, "regular", stakeholder=task_data)
                tasks.append(task)
        return tasks