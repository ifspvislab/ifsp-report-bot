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

from data import Coordinator, CoordinatorData


class CoordinatorAlreadyExists(Exception):
    """
    Exception raised when a coordinator already exists.
    """

    print(Exception)


class ProntuarioError(Exception):
    """
    Exception raised when an incorrect prontuario is encountered.
    """

    print(Exception)


class EmailError(Exception):
    """
    Exception raised when an invalid email is encountered.
    """

    print(Exception)


class DiscordIdError(Exception):
    """
    Exception raised when an invalid Discord ID is encountered.
    """

    print(Exception)


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

    def verify_prontuario(self, value):
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
            raise ProntuarioError("Prontuario incorreto")

        print("Prontuario correto")

    def verify_email(self, value):
        """
        Verify the validity of an email address.

        :param value: The email address to be verified.
        :raises EmailError: If the email address is invalid.
        """
        if not validate_email(value, check_mx=True):
            raise EmailError("Email inválido")

        print("Email correto")

    def verify_discord_id(self, value):
        """
        Verify the validity of a Discord ID.

        :param value: The Discord ID to be verified.
        :raises DiscordIdError: If the Discord ID is invalid.
        """
        if not value.isnumeric():
            raise DiscordIdError("Discord ID inválido")

        print("Discord ID correto")

    def check_ocurrance(self, prontuario):
        """
        Check if a coordinator with the given prontuario already exists.

        :param prontuario: The prontuario to check for existence.
        :raises ValueError: If a coordinator with the given prontuario already exists.
        """
        for coordinator in self.coordinator_data.load_coordinators():
            if prontuario == coordinator.prontuario:
                raise ValueError("Já existe esse membro")

    def create(self, coordenador: Coordinator):
        """
        Create a new coordinator.

        :param coordenador: The Coordinator object representing the new coordinator.
        :raises ProntuarioError: If the prontuario is incorrect.
        :raises EmailError: If the email address is invalid.
        :raises DiscordIdError: If the Discord ID is invalid.
        :raises ValueError: If a coordinator with the given prontuario already exists.
        """
        self.verify_prontuario(coordenador.prontuario)
        self.verify_email(coordenador.email)
        self.verify_discord_id(coordenador.discord_id)
        self.check_ocurrance(coordenador.prontuario)
        coordinator = Coordinator(
            coordenador.prontuario,
            coordenador.discord_id,
            coordenador.name,
            coordenador.email,
        )
        self.coordinator_data.add_coordinator(coordinator)
