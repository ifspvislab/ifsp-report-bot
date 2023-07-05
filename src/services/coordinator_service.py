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

from .validation import verify_discord_id, verify_email, verify_registration_format

logger = settings.logging.getLogger(__name__)


class CoordinatorAlreadyExists(Exception):
    """
    Exception raised when a coordinator already exists.
    """


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

    def check_ocurrance(self, registration):
        """
        Check if a coordinator with the given prontuario already exists.

        :param prontuario: The prontuario to check for existence.
        :raises ValueError: If a coordinator with the given prontuario already exists.
        """
        for coordinator in self.database:
            if registration == coordinator.registration:
                raise CoordinatorAlreadyExists(
                    "ERRO: Já há um coordenador com este prontuário!"
                )

    def create(self, coordenador: Coordinator):
        """
        Create a new coordinator.

        :param coordenador: The Coordinator object representing the new coordinator.
        :raises ProntuarioError: If the prontuario is incorrect.
        :raises EmailError: If the email address is invalid.
        :raises DiscordIdError: If the Discord ID is invalid.
        :raises ValueError: If a coordinator with the given prontuario already exists.
        """
        verify_registration_format(coordenador.registration)
        verify_email(coordenador.email)
        verify_discord_id(coordenador.discord_id)
        self.check_ocurrance(coordenador.registration)
        coordinator = Coordinator(
            coordenador.coord_id,
            coordenador.registration,
            coordenador.discord_id,
            coordenador.name,
            coordenador.email,
        )
        self.coordinator_data.add_coordinator(coordinator)
        self.database.append(coordinator)
