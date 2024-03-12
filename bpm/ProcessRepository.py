from typing import Dict, Optional
from bpm.ProcessDefinition import ProcessDefinition
from bpm.PersistenceLayer import PersistenceLayer


class ProcessRepository:
    """Repository for storing and retrieving process definitions."""
    def __init__(self, persistence_layer: 'PersistenceLayer'):
        self.persistence_layer = persistence_layer
        self.processes: Dict[str, ProcessDefinition] = {}

    def store_process(self, process: ProcessDefinition):
        """Store a process definition."""
        self.processes[process.process_code] = process
        self.persistence_layer.save_state(process)

    def load_process(self, process_code: str) -> Optional[ProcessDefinition]:
        """Load a process definition by process code."""
        if process_code in self.processes:
            return self.processes[process_code]
        else:
            process = self.persistence_layer.load_state(process_code)
            if process:
                self.processes[process_code] = process
                return process
        return None

    def load_processes(self):
        """Load all process definitions from the persistence layer."""
        pass
