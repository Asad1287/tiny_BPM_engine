from typing import Optional
from bpm.PersistenceLayer import PersistenceLayer
from bpm.Stakeholder import Stakeholder
from bpm.Task import Task

class StakeholderManager:
    """Manages stakeholders and their assignments to tasks."""
    def __init__(self, persistence_layer: 'PersistenceLayer'):
        self.persistence_layer = persistence_layer

    def assign_stakeholder(self, task: 'Task', stakeholder: 'Stakeholder'):
        """Assign a stakeholder to a task."""
        pass

    def forward_task(self, task: 'Task', new_stakeholder: 'Stakeholder'):
        """Forward a task to a new stakeholder."""
        pass

    def get_next_stakeholder(self, task: 'Task', current_stakeholder: str) -> Optional[str]:
        """Get the next stakeholder for a task based on the current stakeholder."""
        stakeholders = task.stakeholders
        current_index = list(stakeholders.keys()).index(current_stakeholder)
        next_index = (current_index + 1) % len(stakeholders)
        return list(stakeholders.keys())[next_index]