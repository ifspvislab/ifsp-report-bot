"""
This module provides classes and exceptions for managing coordinators.

Classes:
    CoordinatorAlreadyExists: Exception raised when a coordinator already exists.
    ProntuarioError: Exception raised when an incorrect prontuario is encountered.
    EmailError: Exception raised when an invalid email is encountered.
    DiscordIdError: Exception raised when an invalid Discord ID is encountered.
    CoordinatorService: A service for managing coordinators.

"""

from validate_email_address import validate_email

import settings
from data import Coordinator, CoordinatorData

logger = settings.logging.getLogger(__name__)


class CoordinatorAlreadyExists(Exception):
    """
    Exception raised when a coordinator already exists.
    """


class RegistrationError(Exception):
    """
    Exception raised when an incorrect prontuario is encountered.
    """


class EmailError(Exception):
    """
    Exception raised when an invalid email is encountered.
    """


class DiscordIdError(Exception):
    """
    Exception raised when an invalid Discord ID is encountered.
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

    def verify_registration(self, value):
        """
        Verify the correctness of a prontuario.

        :param value: The prontuario value to be verified.
        :raises ProntuarioError: If the prontuario is incorrect.
        """
        if not (
            value[:1].isalpha()
            and value[2:-2].isnumeric()
            and value[-1].isalnum()
            and len(value) == 9
        ):
            raise RegistrationError("ERRO: Prontuario incorreto")

    def verify_email(self, value):
        """
        Verify the validity of an email address.

        :param value: The email address to be verified.
        :raises EmailError: If the email address is invalid.
        """
        if not validate_email(value, check_mx=True):
            raise EmailError("ERRO: Email inválido")

    def verify_discord_id(self, value):
        """
        Verify the validity of a Discord ID.

        :param value: The Discord ID to be verified.
        :raises DiscordIdError: If the Discord ID is invalid.
        """
        if not value.isnumeric():
            raise DiscordIdError("ERRO: Discord ID inválido")

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
        self.verify_registration(coordenador.registration)
        self.verify_email(coordenador.email)
        self.verify_discord_id(coordenador.discord_id)
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
