"""
member_service
===============

This module provides the class for managing member data 

Class:
    - MemberService: Service class for managing member data
"""

from data import load_members
from validate_email_address import validate_email


class MemberService:
    """
    Service class for managing member data.

    Attributes:
        _prontuario (str): The prontuario (identification number) of the member.
        _name (str): The name of the member.
        _email (str): The email address of the member.
        _discord_id (str): The Discord ID of the member.

    Methods:
        __init__:
            Initializes a new instance of the MemberService class.
        prontuario:
            The prontuario (identification number) property of the member.
        email:
            The email property of the member.
        discord_id:
            The Discord ID property of the member.
        _check_ocurrance:
            Checks if the member already exists in the system.
        verify_standarts:
            Verifies the standards of the member's properties and adds the member to the system.
    """

    def __init__(self, prontuario, name, email, discord_id):
        """
        Initializes a new instance of the MemberService class.

        Args:
            prontuario: The prontuario (identification number) of the member.
            name: The name of the member.
            email: The email address of the member.
            discord_id: The Discord ID of the member.
        """
        self._prontuario = prontuario
        self._name = name
        self._email = email
        self._discord_id = discord_id
        self._stats = []

    @property
    def prontuario(self):
        """
        Get or set the prontuario (identification number) property of the member.

        Returns:
            The prontuario of the member.
        """
        return self._prontuario

    @prontuario.setter
    def prontuario(self, value):
        """
        Set the prontuario (identification number) property of the member.

        Args:
            value: The new prontuario value to set.

        Raises:
            ValueError: If the provided prontuario is incorrect.
        """
        if not (
            value[:1].isalpha()
            and value[2:-2].isnumeric()
            and value[-1].isalnum()
            and len(value) == 9
        ):
            self._stats.append("Prontuario incorreto")
        self._prontuario = value

    @property
    def email(self):
        """
        Get or set the email property of the member.

        Returns:
            The email address of the member.
        """
        return self._email

    @email.setter
    def email(self, value):
        """
        Set the email property of the member.

        Args:
            value: The new email address value to set.

        Raises:
            ValueError: If the provided email is invalid.
        """
        if not validate_email(value):
            self._stats.append("email inválido")
        self._email = value

    @property
    def discord_id(self):
        """
        Get or set the Discord ID property of the member.

        Returns:
            The Discord ID of the member.
        """
        return self._discord_id

    @discord_id.setter
    def discord_id(self, value):
        """
        Set the Discord ID property of the member.

        Args:
            value: The new Discord ID value to set.

        Raises:
            ValueError: If the provided Discord ID is invalid.
        """
        if not value.isnumeric():
            self._stats.append("discord_id inválido")
        self._discord_id = value

    def _check_ocurrance(self) -> str:
        """
        Checks if the member already exists in the system.

        Raises:
            ValueError: If the member already exists.
        """
        for members in load_members():
            if self._prontuario == members["prontuario"]:
                return "Já existe esse membro"

    def verify_standarts(self, member) -> str:
        """
        Verifies the standards of the member's properties.

        Args:
            member: The member containing member properties.

        Raises:
            ValueError: If any of the member properties are invalid or the member already exists.
        """
        self._stats = []
        self.prontuario = member.prontuario.value
        self.email = member.email.value
        self.discord_id = member.discord_id.value
        if self._check_ocurrance() != None:
            self._stats.append(self._check_ocurrance())
        if self._stats == []:
            self._stats.append("Membro cadastrado com sucesso.")
        else:
            self._stats.append("Infelismente não foi possivel cadastrar.")

        return self._stats
