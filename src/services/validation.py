"""
validation module
"""
from validate_email_address import validate_email

from data import Member, Project


class CoordinatorRegistrationError(Exception):
    """
    Exception raised when an incorrect coordinator registration is encountered.
    """


class RegistrationError(Exception):
    """
    Exception raised when an incorrect registration is encountered.
    """


class EmailError(Exception):
    """
    Exception raised when an invalid email is encountered.
    """


class DiscordIdError(Exception):
    """
    Exception raised when an invalid Discord ID is encountered.
    """


class MemberError(Exception):
    """
    Exception raised when an member isn't encountered.
    """

def verify_coordinator_registration_format(coordinator_id):
    """
    Verify the correctness of a prontuario.

    :param value: The registration value to be verified.
    :raises CoordinatorRegistrationError: If the registration is incorrect.
    """
    if not (
        coordinator_id[:1].isalpha()
        and coordinator_id[2:-2].isnumeric()
        and coordinator_id[-1].isalnum()
        and len(coordinator_id) == 9
    ):
        raise CoordinatorRegistrationError("Prontuário do Coordenador incorreto")


def verify_registration_format(registration):
    """
    Verify the correctness of a prontuario.

    :param value: The prontuario value to be verified.
    :raises ProntuarioError: If the prontuario is incorrect.
    """
    if not (
        registration[:1].isalpha()
        and registration[2:-2].isnumeric()
        and registration[-1].isalnum()
        and len(registration) == 9
    ):
        raise RegistrationError("Prontuário incorreto")


def verify_email(value):
    """Verify the correctness of the email address.

    Args:
        value (str): The email address value to be verified.

    Raises:
        EmailError: If the email address is invalid.
    """
    if not validate_email(value, check_mx=False):
        raise EmailError("Email inválido")


def verify_discord_id(value):
    """Verify the correctness of the Discord ID.

    Args:
        value (str): The Discord ID value to be verified.

    Raises:
        DiscordIdError: If the Discord ID is invalid.
    """
    if not value.isnumeric():
        raise DiscordIdError("Discord ID inválido")


def verify_member_exists(value, membros: list[Member]):
    """
    Verify if the member exists in the registers.
    Args:
        value(str): The registration to be verified.
        membros: A list with all members in the registers.

    Raises:
        MemberError: If the member isn't in the registers.
    """

    members = membros
    for member in members:
        if member.registration == value:
            return None

    raise MemberError("O membro inexiste nos registros!")
