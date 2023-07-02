"""
project_service
=======================

This module provides the classes and exceptions for managing project data.

Classes:

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
