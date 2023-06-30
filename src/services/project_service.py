# pylint: skip-file

"""
project_service
=======================
This module provides the classes and exceptions for managing project data.
Classes:
    - InvalidCoordinator: Exception that checks if the coordinator exists.
    - EqualOrSmallerDateError: Exception that checks if the end date is smaller or equal the start date.
    - InvalidTimeInterval: Exception that checks if the time interval between the end date and the start date is greater than 1 month.
    - InvalidEndDate: Exception that checks if the end date is less than the current data.
    - DiscordServerIdError: Exception that checks if the Discord Server ID is invalid.
    - ProjectAlreadyExists: Exception that checks if the project already exists.
"""

from data.project_data import Project


class ProjectService:
    def find_project_by_type(self, attr_type, value) -> Project | None:
        return Project("aaaaa", "oooooo", 123132, "abba", 1, 2)
