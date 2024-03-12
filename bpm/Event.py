from typing import Dict
from bpm.ProcessInstance import ProcessInstance
class Event:
    """Represents an event in the workflow."""
    def __init__(self, type: str, data: Dict[str, 'ProcessInstance']):
        self.type = type
        self.data = data
