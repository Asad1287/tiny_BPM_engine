from typing import Optional
from bpm.ProcessDefinition import ProcessDefinition
from bpm.ProcessRepository import ProcessRepository


class ProcessManager:
    """Manages process definitions and instances."""
    def __init__(self, process_repository: 'ProcessRepository'):
        self.process_repository = process_repository

    def load_process(self, process_code: str) -> Optional[ProcessDefinition]:
        """Load a process definition by process code."""
        return self.process_repository.load_process(process_code)

    def get_process_definition(self):
        """Retrieve the process definition."""
        pass

    def validate_process(self, process: ProcessDefinition):
        """Validate the process definition."""
        pass