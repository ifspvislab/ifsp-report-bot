"""
services
=======

This package provides services for managing student data.

Modules:
    - student_service: Module for managing student data.

"""
from .coordinator_service import is_coordinator
from .log_service import IncorrectDateFilter, LogService
from .student_service import StudentService
