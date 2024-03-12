from typing import Optional, Union
from bpm.Database import Database
from bpm.ProcessDefinition import ProcessDefinition
from bpm.ProcessInstance import ProcessInstance
from bpm.Task import Task
from bpm.Stakeholder import Stakeholder



class PersistenceLayer:
    """Persistence layer for storing and retrieving workflow state."""
    def __init__(self, db: Database):
        self.db = db

    def load_process_definition(self, process_code: str) -> Optional[ProcessDefinition]:
        """Load a process definition from the database."""
        self.db.cursor.execute("""
            SELECT process_code, process_name, process_description
            FROM processes            WHERE process_code = ?
        """, (process_code,))
        process_data = self.db.cursor.fetchone()

        if process_data:
            process_code, process_name, process_description = process_data

            self.db.cursor.execute("""
                SELECT task_id, task_name, task_type, stakeholder
                FROM tasks
                WHERE process_code = ?
            """, (process_code,))
            task_data_list = self.db.cursor.fetchall()

            tasks = []
            for task_data in task_data_list:
                task_id, task_name, task_type, stakeholder = task_data
                task = Task(task_id, task_name, task_type, stakeholder=stakeholder)
                tasks.append(task)

            self.db.cursor.execute("""
                SELECT stakeholder_id, type, name, email, department, contact_email
                FROM stakeholders
            """)
            stakeholder_data_list = self.db.cursor.fetchall()

            stakeholders = {}
            for stakeholder_data in stakeholder_data_list:
                stakeholder_id, type, name, email, department, contact_email = stakeholder_data
                
                if type == "group":
                    self.db.cursor.execute("""
                        SELECT member
                        FROM group_members
                        WHERE stakeholder_id = ?
                    """, (stakeholder_id,))
                    member_data_list = self.db.cursor.fetchall()
                    members = [member[0] for member in member_data_list]
                else:
                    members = None
                
                stakeholder = Stakeholder(type, name, email, department, contact_email, members)
                stakeholders[stakeholder_id] = stakeholder

            return ProcessDefinition(process_code, process_name, process_description, tasks, stakeholders)
        else:
            return None

    def save_state(self, state: Union[ProcessInstance, ProcessDefinition]):
        """Save the state of a process instance or definition."""
        if isinstance(state, ProcessInstance):
            key = state.definition.process_code
        elif isinstance(state, ProcessDefinition):
            key = state.process_code
        else:
            raise ValueError("Unsupported state type")

    def load_state(self, process_code: str) -> Optional[Union[ProcessInstance, ProcessDefinition]]:
        """Load the state of a process instance or definition by process code."""
        return self.states.get(process_code)