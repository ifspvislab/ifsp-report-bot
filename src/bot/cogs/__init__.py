"""
A package for managing cogs
===========================

Package Structure
-----------------
- add_member: Module for add_member functionality interface.
"""

from .add_coordinator import CoordinatorCog
from .add_member import MemberCog
from .add_participation import ParticipationCog
from .add_project import ProjectCog
from .attendance_cog import AttendanceCog
from .events import Events
from .log_command import LogCommand
from .monthly_report_cog import MonthlyReportCog
from .semester_report_cog import SemesterReportCog
from .termination_statement_cog import TerminationStatementCog
