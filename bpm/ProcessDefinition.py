from typing import List, Dict
from bpm.Task import Task
from bpm.Stakeholder import Stakeholder

class ProcessDefinition:
    """Represents a process definition."""
    def __init__(self, process_code: str, process_name: str, process_description: str, tasks: List[Task],
                 stakeholders: Dict[str, Stakeholder]):
        self.process_code = process_code
        self.process_name = process_name
        self.process_description = process_description
        self.tasks = tasks
        self.stakeholders = stakeholders