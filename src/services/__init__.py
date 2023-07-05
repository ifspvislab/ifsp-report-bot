"""
services
=======

This package provides services for managing student data.

Modules:
    - member_service: Module for managing member data.
    - student_service: Module for managing student data.

"""

from .admin_service import is_admin
from .coordinator_service import (
    Coordinator,
    CoordinatorAlreadyExists,
    CoordinatorService,
)
from .member_service import MemberService
from .project_service import (
    DiscordServerIdError,
    EqualOrSmallerDateError,
    InvalidCoordinator,
    InvalidEndDate,
    InvalidTimeInterval,
    Project,
    ProjectAlreadyExists,
    ProjectService,
)
from .student_service import StudentService
from .validation import DiscordIdError, EmailError, RegistrationError
