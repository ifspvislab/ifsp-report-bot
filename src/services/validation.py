"""
validation module
"""
from validate_email_address import validate_email


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


def verify_registration(value):
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


def verify_email(value):
    """Verify the correctness of the email address.

    Args:
        value (str): The email address value to be verified.

    Raises:
        EmailError: If the email address is invalid.
    """
    if not validate_email(value, check_mx=True):
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
