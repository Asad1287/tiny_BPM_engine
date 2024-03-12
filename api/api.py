from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import the necessary classes and functions from your existing codebase
from database import Database
from data_loader import DataLoader
from persistence_layer import PersistenceLayer
from process_repository import ProcessRepository
from stakeholder_manager import StakeholderManager
from task_processor import TaskProcessor
from event_dispatcher import EventDispatcher
from process_manager import ProcessManager
from workflow_engine import WorkflowEngine

app = FastAPI()

# Initialize the database and load the process and stakeholder data
db = Database("workflow.db")
db.create_tables()
data_loader = DataLoader("process.json", "stakeholder.json")
process_definition = data_loader.load_data()

# Create instances of the necessary classes
persistence_layer = PersistenceLayer(db)
process_repository = ProcessRepository(persistence_layer)
stakeholder_manager = StakeholderManager(persistence_layer)
task_processor = TaskProcessor(stakeholder_manager)
event_dispatcher = EventDispatcher(db)
process_manager = ProcessManager(process_repository)
workflow_engine = WorkflowEngine(process_manager, event_dispatcher, task_processor, stakeholder_manager, persistence_layer)

# Store the process definition in the process repository
process_repository.store_process(process_definition)

# Define request models
class RouteRequest(BaseModel):
    action: str
    task_id: str

class RouteResponse(BaseModel):
    message: str

# API endpoint for routing tasks
@app.post("/route", response_model=RouteResponse)
def route_task(request: RouteRequest):
    action = request.action.upper()
    task_id = request.task_id

    if action == "ROUTE":
        process_instance = workflow_engine.get_process_instance(process_definition.process_code)
        if process_instance is None:
            process_instance = workflow_engine.create_process_instance(process_definition)

        current_task = process_instance.get_task_by_id(task_id)
        if current_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        if current_task.task_id != process_instance.get_current_task().task_id:
            raise HTTPException(status_code=400, detail="Invalid task sequence")

        workflow_engine.route_task(process_instance, current_task)
        persistence_layer.save_state(process_instance)

        if process_instance.is_completed():
            return {"message": "Process completed"}
        else:
            next_task = process_instance.get_current_task()
            return {"message": f"Task {current_task.task_id} routed. Waiting for task {next_task.task_id}"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

# API endpoint for getting the current task
@app.get("/current-task", response_model=Optional[str])
def get_current_task():
    process_instance = workflow_engine.get_process_instance(process_definition.process_code)
    if process_instance is None or process_instance.is_completed():
        return None
    else:
        current_task = process_instance.get_current_task()
        return current_task.task_id