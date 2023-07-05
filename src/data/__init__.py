"""
A package for managing project data and members
================================================

Package Structure
-----------------
- ``member_data``: Module for managing member data.
- ``coordinator_data``: Module for managing coordinator data.
- ``project_data``: Module for managing project data.
- ``student_data``: Module for managing student data.
"""

from .member_data import Member
from .project_data import Project
from .participation_data import Participation
from .coordinator_data import Coordinator
from .data import load_students
