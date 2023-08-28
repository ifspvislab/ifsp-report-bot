"""
services
=======

This package provides services for managing student data.

Modules:
    - member_service: Module for managing member data.
    - student_service: Module for managing student data.
"""

from .admin_service import is_admin
from .attendance_service import AttendanceService
from .coordinator_service import (Coordinator, CoordinatorAlreadyExists,
                                  CoordinatorService)
from .log_service import (IdDoesNotExist, IncorrectDateFilter,
                          InvalidReportSize, LogService, NoStartDate)
from .member_service import MemberService
from .monthly_report_service import MonthlyReportService
from .participation_service import (DateError, MemberError,
                                    ParticipationAlreadyExists,
                                    ParticipationService, ProjectError)
from .project_service import (DiscordServerIdError, EqualOrSmallerDateError,
                              InvalidCoordinator, InvalidEndDate,
                              InvalidTimeInterval, Project,
                              ProjectAlreadyExists, ProjectService)
from .report_service import ReportService
from .termination_service import (CoordinatorNotFound, InvalidDayForMonth,
                                  InvalidLiteralTerminationDate, InvalidMonth,
                                  MemberNotFound, OutofRangeTerminationDate,
                                  ParticipationNotFound,
                                  ParticipationNotFoundInServer,
                                  ProjectNotFound, SlashAbsence,
                                  TerminationStatementService, YearOutOfRange)
from .validation import DiscordIdError, EmailError, RegistrationError
