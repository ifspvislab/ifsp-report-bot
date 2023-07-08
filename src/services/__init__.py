"""
services
=======

This package provides services for managing student data.

Modules:
    - student_service: Module for managing student data.

"""
from .coordinator_service import CoordinatorAlreadyExists, CoordinatorService
from .is_coordinator import is_coordinator
from .log_service import (
    IdDoesNotExist,
    IncorrectDateFilter,
    InvalidReportSize,
    LogService,
    NoStartDate,
)
from .member_service import MemberService
from .participation_service import (
    DateError,
    ParticipationAlreadyExists,
    ParticipationService,
)
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
from .validation import DiscordIdError, EmailError, MemberError, RegistrationError
