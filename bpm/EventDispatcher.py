from datetime import datetime
from typing import Dict, List, Union
from bpm.Database import Database
from bpm.Event import Event
from bpm.WorkflowEngine import WorkflowEngine
from bpm.TaskProcessor import TaskProcessor

class EventDispatcher:
    """Dispatches events to subscribed components."""
    def __init__(self, db: Database):
        self.db = db
        self.subscribers: Dict[str, List[Union[WorkflowEngine, TaskProcessor]]] = {}

    def dispatch_event(self, event: Event):
        """Dispatch an event to subscribed components."""
        for subscriber in self.subscribers.get(event.type, []):
            subscriber.handle_event(event)

        # Record the event in the database
        if event.type == "task_assigned":
            process_instance = event.data["process_instance"]
            task = event.data["task"]
            stakeholder_action = "ASSIGNED"
            date_assigned = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_completed = ""
            self.db.record_transaction(process_instance.definition.process_code,
                                       process_instance.definition.process_name,
                                       task.task_id, task.task_name, stakeholder_action,
                                       date_assigned, date_completed)
        elif event.type == "task_completed":
            process_instance = event.data["process_instance"]
            task = event.data["task"]
            stakeholder_action = "COMPLETED"
            date_assigned = ""
            date_completed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.record_transaction(process_instance.definition.process_code,
                                       process_instance.definition.process_name,
                                       task.task_id, task.task_name, stakeholder_action,
                                       date_assigned, date_completed)

    def subscribe(self, component: Union[WorkflowEngine, TaskProcessor], events: List[str]):
        """Subscribe a component to specified events."""
        for event in events:
            self.subscribers.setdefault(event, []).append(component)
