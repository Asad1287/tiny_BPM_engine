from bpm.Database import Database
from bpm.Dataloader import DataLoader
from bpm.PersistenceLayer import PersistenceLayer
from bpm.ProcessRepository import ProcessRepository
from bpm.StakeholderManager import StakeholderManager
from bpm.TaskProcessor import TaskProcessor
from bpm.EventDispatcher import EventDispatcher
from bpm.ProcessManager import ProcessManager
from bpm.WorkflowEngine import WorkflowEngine
from bpm.WorkflowRouter import WorkflowRouter


def main():
    # Create the database and tables
    db = Database("workflow.db")
    db.create_tables()

    # Load the process and stakeholder data using the DataLoader
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

    # Create an instance of the WorkflowRouter
    workflow_router = WorkflowRouter(workflow_engine)

    # Start the workflow routing
    process_code = "P001"  # Replace with the desired process code
    workflow_router.route_workflow(process_code)


if __name__ == "__main__":
    main()