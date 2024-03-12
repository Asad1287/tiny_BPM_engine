from bpm.WorkflowEngine import WorkflowEngine
class CommandLineInterface:
    """Command-line interface for interacting with the workflow engine."""
    def __init__(self, workflow_engine: WorkflowEngine):
        self.workflow_engine = workflow_engine

    def parse_command(self, command: str):
        """Parse the command and invoke the appropriate method on the workflow engine."""
        pass