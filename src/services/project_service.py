"""
project_service
=======================

This module provides the classes and exceptions for managing project data.

Classes:
    - InvalidCoordinator: Exception raised when coordinator does not manage any projects.
    - EqualOrSmallerDateError: Exception raised when the end date is equal or 
    less than the start date.
    - InvalidTimeInterval: Exception raised when the time interval 
    between the end date and the start date is less than than 1 month.
    - InvalidEndDate: Exception raised when the end date is less than the current data.
    - DiscordServerIdError: Exception raised when the Discord Server ID is invalid.
    - ProjectAlreadyExists: Exception raised when the project already exists.
"""

import settings
from data.project_data import ProjectData

logger = settings.logging.getLogger(__name__)

# pylint: disable=too-few-public-methods
class ProjectService:
    """
    A service for managing projects.
    """

    def __init__(self, project_data: ProjectData):
        """
        Initializes the ProjectService instance.

        Args:
            project_data (ProjectData): The project data object for managing project data.
        """
        self.project_data = project_data

        self.database = self.project_data.load_projects()

    def find_project_by_type(self, attr_type, value):
        """
        Finds a project by the specified attribute type and value.

        Args:
            attr_type (str): The attribute type to search for.
            value: The value to match with the attribute.

        Returns:
            Project or None: The matching project or None if not found.
        """
        for project in self.database:
            if getattr(project, attr_type) == value:
                return project

        return None
