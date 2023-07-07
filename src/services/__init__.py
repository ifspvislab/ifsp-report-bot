"""
services
=======

This package provides services for managing student data.

Modules:
    - member_service: Module for managing member data.
    - student_service: Module for managing student data.

"""
from .coordinator_service import CoordinatorService
from .member_service import MemberService
from .participation_service import ParticipationService
from .project_service import ProjectService
from .student_service import StudentService
from .termination_service import (
    CoordinatorNotFound,
    InvalidDayForMonth,
    InvalidLiteralTerminationDate,
    InvalidMonth,
    MemberNotFound,
    OutofRangeTerminationDate,
    ParticipationNotFound,
    ParticipationNotFoundInServer,
    ProjectNotFound,
    SlashAbsence,
    TerminationStatementService,
    YearOutOfRange,
)
