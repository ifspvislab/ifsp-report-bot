"""
validation module
"""
from validate_email_address import validate_email


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


def verify_registration_format(registration):
    """
    Verify the correctness of a registration.

    :param value: The registration value to be verified.
    :raises RegistrationError: If the registration is incorrect.
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
    """
    Verify the correctness of the Discord ID.

    Args:
        value (str): The Discord ID value to be verified.

    Raises:
        DiscordIdError: If the Discord ID is invalid.
    """
    if not value.isnumeric():
        raise DiscordIdError("Discord ID inválido")
