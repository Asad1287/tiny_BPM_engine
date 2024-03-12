from typing import List, Optional

class Stakeholder:
    """Represents a stakeholder in the workflow."""
    def __init__(self, type: str, name: str, email: Optional[str] = None, department: Optional[str] = None,
                 contact_email: Optional[str] = None, members: Optional[List[str]] = None):
        self.type = type
        self.name = name
        self.email = email
        self.department = department
        self.contact_email = contact_email
        self.members = members
