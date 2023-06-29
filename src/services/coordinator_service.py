"""
This module provides classes and exceptions for managing coordinators.
Classes:
    CoordinatorService: A service for managing coordinators.
"""

from data import CoordinatorData


# pylint: disable=too-few-public-methods
class CoordinatorService:
    """
    A service for managing coordinators.
    """

    def __init__(self, coordinator_data: CoordinatorData):
        """
        Initialize the CoordinatorService.
        :param coordinator_data: The CoordinatorData object used for data storage.
        """
        self.coordinator_data = coordinator_data
        self.database = self.coordinator_data.load_coordinators(self)

    def find_coordinator_by_type(self, attr_type, value):
        """
        Find a coordinator in the database based on the specified attribute type and value.
        Args:
            attr_type (str): The attribute type to be checked.
            value: The value of the attribute to be matched.
        Returns:
            The coordinator object if found, None otherwise.
        """
        for coordinator in self.database:
            if getattr(coordinator, attr_type) == value:
                return coordinator

        return None
