"""
services
=======

This package provides services for managing student data.

Modules:
    - student_service: Module for managing student data.
    - professor_service: Module for managing professor data.

"""

from .participation_service import (
    DateError,
    InputAlreadyExists,
    ParticipationService,
    ProjectError,
    StudentError,
)
from .student_service import StudentService
