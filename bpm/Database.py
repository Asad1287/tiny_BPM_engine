import sqlite3
from typing import Dict, Any

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS processes (
                process_code TEXT PRIMARY KEY,
                process_name TEXT,
                process_description TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                task_name TEXT,
                task_type TEXT,
                stakeholders_group TEXT,
                stakeholder TEXT,
                process_code TEXT,
                FOREIGN KEY (process_code) REFERENCES processes (process_code)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stakeholders (
                stakeholder_id TEXT PRIMARY KEY,
                type TEXT,
                name TEXT,
                email TEXT,
                department TEXT,
                contact_email TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_code TEXT,
                process_name TEXT,
                task_id TEXT,
                task_name TEXT,
                stakeholder_action TEXT,
                date_assigned TEXT,
                date_completed TEXT,
                FOREIGN KEY (process_code) REFERENCES processes (process_code),
                FOREIGN KEY (task_id) REFERENCES tasks (task_id)
            )
        """)

        self.cursor.execute("""
           CREATE TABLE IF NOT EXISTS group_members (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           stakeholder_id TEXT,
           member TEXT,
           FOREIGN KEY (stakeholder_id) REFERENCES stakeholders (stakeholder_id)
           )
        """)



        self.conn.commit()


    def initialize_data(self, process_data: Dict[str, Any]):
        process_code = process_data["process_code"]
        process_name = process_data["process_name"]
        process_description = process_data["process_description"]

        self.cursor.execute("""
            INSERT OR REPLACE INTO processes (process_code, process_name, process_description)
            VALUES (?, ?, ?)
        """, (process_code, process_name, process_description))

        for task_data in process_data["tasks"]:
            task_id = task_data["task_id"]
            task_name = task_data["task_name"]
            task_type = task_data["task_type"]
            stakeholders_group = task_data.get("stakeholders_group")
            stakeholder = task_data.get("stakeholder")

            self.cursor.execute("""
                INSERT OR REPLACE INTO tasks (task_id, task_name, task_type, stakeholders_group, stakeholder, process_code)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (task_id, task_name, task_type, stakeholders_group, stakeholder, process_code))

        for stakeholder_id, stakeholder_data in process_data["stakeholders"].items():
            type = stakeholder_data.get("type", "individual")
            name = stakeholder_data.get("name")
            email = stakeholder_data.get("email")
            department = stakeholder_data.get("department")
            contact_email = stakeholder_data.get("contact_email")

            self.cursor.execute("""
                INSERT OR REPLACE INTO stakeholders (stakeholder_id, type, name, email, department, contact_email)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (stakeholder_id, type, name, email, department, contact_email))

        self.conn.commit()

    def record_transaction(self, process_code: str, process_name: str, task_id: str, task_name: str,
                           stakeholder_action: str, date_assigned: str, date_completed: str):
        self.cursor.execute("""
            INSERT INTO transactions (process_code, process_name, task_id, task_name, stakeholder_action,
                                      date_assigned, date_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (process_code, process_name, task_id, task_name, stakeholder_action, date_assigned, date_completed))
        self.conn.commit()

    def close(self):
        self.conn.close()