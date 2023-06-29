"""
services
=======

This package provides services for managing student data.

Modules:
    - student_service: Module for managing student data.

"""
from .admin_service import is_admin
from .project_service import (
    DiscordServerIdError,
    EqualOrSmallerDateError,
    InvalidCoordinator,
    InvalidEndDate,
    InvalidTimeInterval,
    ProjectAlreadyExists,
    is_admin,
)
from .student_service import StudentService
