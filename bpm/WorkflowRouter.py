from bpm.ProcessInstance import ProcessInstance
from bpm.WorkflowEngine import WorkflowEngine
from bpm.Task import Task
from bpm.Stakeholder import Stakeholder



class WorkflowRouter:
    def __init__(self, workflow_engine: WorkflowEngine):
        self.workflow_engine = workflow_engine

    def route_workflow(self, process_code: str):
        process_definition = self.load_process_definition(process_code)
        if process_definition is None:
            print(f"Process '{process_code}' not found.")
            return

        process_instance = ProcessInstance(process_definition)
        current_task_index = 0

        while current_task_index < len(process_instance.definition.tasks):
            current_task = process_instance.definition.tasks[current_task_index]
            self.display_current_task(current_task)

            if current_task.task_type == "choice" and current_task.options:
                current_task = self.handle_choice_task(current_task)

            stakeholder = self.get_stakeholder(process_instance, current_task)
            if stakeholder is None:
                break

            action = self.get_user_action()
            if action == "ROUTE":
                current_task_index += 1
            elif action == "RETURNED":
                current_task_index = 0
            elif action == "CANCEL":
                print("Workflow cancelled.")
                break
            else:
                print("Invalid action. Please try again.")

    def load_process_definition(self, process_code: str):
        return self.workflow_engine.persistence_layer.load_process_definition(process_code)

    def display_current_task(self, task: Task):
        print(f"Current task: {task.task_name}")

    def handle_choice_task(self, task: Task):
        print("Available options:")
        for index, option in enumerate(task.options, start=1):
            print(f"{index}. {option.task_name}")

        while True:
            try:
                choice = int(input("Enter the option number: ")) - 1
                if 0 <= choice < len(task.options):
                    return task.options[choice]
                else:
                    print("Please enter a valid option number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_stakeholder(self, process_instance: ProcessInstance, task: Task):
        stakeholder_id = task.stakeholder
        if stakeholder_id in process_instance.definition.stakeholders:
            stakeholder = process_instance.definition.stakeholders[stakeholder_id]
            self.display_stakeholder_info(stakeholder)
            return stakeholder
        else:
            print(f"Stakeholder '{stakeholder_id}' not found.")
            return None

    def display_stakeholder_info(self, stakeholder: Stakeholder):
        if stakeholder.type == "group":
            print(f"Current stakeholder group: {stakeholder.name}")
            print("Group members:")
            for member in stakeholder.members:
                print(member)
        else:
            print(f"Current stakeholder: {stakeholder.name}")

    def get_user_action(self):
        return input("Enter the action (ROUTE/RETURNED/CANCEL): ").upper()