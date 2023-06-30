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

import settings
from data import Member, MemberData

logger = settings.logging.getLogger(__name__)


class MemberAlreadyExists(Exception):
    """Exception raised when a member already exists."""

    print(Exception)


class RegistrationError(Exception):
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
        self.database = self.member_data.load_members()

    def find_member_by_type(self, attr_type, value):
        """
        Find a member in the database based on the specified attribute type and value.

        Args:
            attr_type (str): The attribute type to be checked.
            value: The value of the attribute to be matched.

        Returns:
            The member object if found, None otherwise.
        """
        for member in self.database:
            if getattr(member, attr_type) == value:
                return member

        return None

    def verify_registration(self, value):
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
            raise RegistrationError("Prontuario incorreto")

    def verify_email(self, value):
        """Verify the correctness of the email address.

        Args:
            value (str): The email address value to be verified.

        Raises:
            EmailError: If the email address is invalid.
        """
        if not validate_email(value, check_mx=True):
            raise EmailError("Email inválido")

    def verify_discord_id(self, value):
        """Verify the correctness of the Discord ID.

        Args:
            value (str): The Discord ID value to be verified.

        Raises:
            DiscordIdError: If the Discord ID is invalid.
        """
        if not value.isnumeric():
            raise DiscordIdError("Discord ID inválido")

    def check_ocurrance(self, registration):
        """Check if a member with the given prontuario already exists.

        Args:
            value (str): The prontuario value to check.

        Raises:
            OccurrenceError: If a member with the same prontuario already exists.
        """

        if self.find_member_by_type("registration", registration):
            raise OccurrenceError("Já existe esse membro")

    def add_member(self, member):
        """Add a new member.

        Args:
            member (Member): Member object.
        """
        self.verify_registration(member.registration)
        self.verify_email(member.email)
        self.verify_discord_id(member.discord_id)
        self.check_ocurrance(member.registration)
        member = Member(
            member.member_id,
            member.registration,
            member.discord_id,
            member.name,
            member.email,
        )
        self.member_data.add_member(member)
        self.database.append(member)
