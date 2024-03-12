from typing import Any, List, Optional

class Task:
    def __init__(self, task_id: str, task_name: str, task_type: str, stakeholder: Optional[str] = None, options: Optional[List[Any]] = None):
        self.task_id = task_id
        self.task_name = task_name
        self.task_type = task_type
        self.stakeholder = stakeholder
        self.options = options or []
