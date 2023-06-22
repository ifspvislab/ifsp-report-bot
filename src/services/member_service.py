"""
services
=======

This package provides services for managing student data.

Modules
-------
.. autosummary::
    :toctree: generated/

    member_service
    student_service

Usage
-----

Import specific modules from the package:

.. code-block:: python

    from services import MemberService, StudentService

Use the imported modules to manage student data.

"""

from validate_email_address import validate_email

from data import Member, MemberData


class MemberAlreadyExists(Exception):
    """Exception raised when a member already exists."""

    print(Exception)


class ProntuarioError(Exception):
    """Exception raised when there is an error with the prontuario."""

    print(Exception)


class EmailError(Exception):
    """Exception raised when there is an error with the email."""

    print(Exception)


class DiscordIdError(Exception):
    """Exception raised when there is an error with the Discord ID."""

    print(Exception)


class OccurrenceError(Exception):
    """Exception raised when there is a duplicate occurrence of a member."""

    print(Exception)


class MemberService:
    """Class for managing member data.

    Args:
        member_data (MemberData): An instance of MemberData class for accessing member data.

    Attributes:
        member_data (MemberData): An instance of MemberData class for accessing member data.
    """

    def __init__(self, member_data: MemberData):
        self.member_data = member_data

    def verify_prontuario(self, value):
        """Verify the correctness of the prontuario.

        Args:
            value (str): The prontuario value to be verified.

        Raises:
            ProntuarioError: If the prontuario is incorrect.
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
        """Verify the correctness of the email address.

        Args:
            value (str): The email address value to be verified.

        Raises:
            EmailError: If the email address is invalid.
        """
        if not validate_email(value, check_mx=True):
            raise EmailError("Email inválido")

        print("Email correto")

    def verify_discord_id(self, value):
        """Verify the correctness of the Discord ID.

        Args:
            value (str): The Discord ID value to be verified.

        Raises:
            DiscordIdError: If the Discord ID is invalid.
        """
        if not value.isnumeric():
            raise DiscordIdError("Discord ID inválido")

        print("Discord ID correto")

    def check_ocurrance(self, value):
        """Check if a member with the given prontuario already exists.

        Args:
            value (str): The prontuario value to check.

        Raises:
            OccurrenceError: If a member with the same prontuario already exists.
        """

        for member in self.member_data.load_members():
            if value == member.prontuario:
                raise OccurrenceError("Já existe esse membro")

        print("Novo membro")

    def add_member(self, prontuario, discord_id, name, email):
        """Add a new member.

        Args:
            prontuario (str): The prontuario of the member.
            discord_id (int): The Discord ID of the member.
            name (str): The name of the member.
            email (str): The email address of the member.
        """
        self.verify_prontuario(prontuario)
        self.verify_email(email)
        self.verify_discord_id(discord_id)
        self.check_ocurrance(prontuario)
        member = Member(prontuario, discord_id, name, email)
        self.member_data.add_member(member)
