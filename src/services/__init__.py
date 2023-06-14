"""
services
=======

This package provides services for managing student data.

Modules:
    - student_service: Module for managing student data.

"""
from .admin_service import AdminService
from .project_service import DiscordServerIdError, Project, ProjectAlreadyExists
from .student_service import StudentService
