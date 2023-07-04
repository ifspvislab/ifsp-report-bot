"""
This module provides classes and exceptions for managing coordinators.

Classes:
    CoordinatorAlreadyExists: Exception raised when a coordinator already exists.
    ProntuarioError: Exception raised when an incorrect registration is encountered.
    EmailError: Exception raised when an invalid email is encountered.
    DiscordIdError: Exception raised when an invalid Discord ID is encountered.
    CoordinatorService: A service for managing coordinators.

"""

import settings
from data import Coordinator, CoordinatorData

logger = settings.logging.getLogger(__name__)


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
        self.database = self.coordinator_data.load_coordinators()

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

    def create(self, coordenador: Coordinator):
        """
        Create a new coordinator.

        :param coordinator: The Coordinator object representing the new coordinator.
        :raises ProntuarioError: If the registration is incorrect.
        :raises EmailError: If the email address is invalid.
        :raises DiscordIdError: If the Discord ID is invalid.
        :raises ValueError: If a coordinator with the given registration already exists.
        """
        coordinator = Coordinator(
            coordenador.coord_id,
            coordenador.registration,
            coordenador.discord_id,
            coordenador.name,
            coordenador.email,
        )
        self.coordinator_data.add_coordinator(coordinator)
        self.database.append(coordinator)
