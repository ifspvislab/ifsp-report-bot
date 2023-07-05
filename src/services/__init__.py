"""
services
=======

This package provides services for managing student data.

Modules:
    - student_service: Module for managing student data.

"""
from .log_service import IncorrectDateFilter, LogService, NotCoordiantor, is_coordinator
from .student_service import StudentService
from .validation import DiscordIdError
