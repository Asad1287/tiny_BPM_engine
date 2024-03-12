from typing import Optional
from bpm.ProcessDefinition import ProcessDefinition
from bpm.Task import Task

class ProcessInstance:
    """Represents an instance of a process."""
    def __init__(self, definition: ProcessDefinition):
        self.definition = definition
        self.current_task: Optional[Task] = None