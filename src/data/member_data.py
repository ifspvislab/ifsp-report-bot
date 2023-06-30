"""
:mod: member_data
=================
Module for managing member data stored in a CSV file.
Module Dependencies:
    - ``csv``: A module for working with CSV files.
Classes:
    - :class:`MemberData`: Class for managing member data.
"""

from dataclasses import dataclass


@dataclass
class Member:
    """Class representing a member.
    Attributes:
        member_id(str): The ID of the member.
        prontuario (str): The prontuario of the member.
        discord_id (int): The Discord ID of the member.
        name (str): The name of the member.
        email (str): The email address of the member.
    """

    member_id: str
    prontuario: str
    discord_id: int
    name: str
    email: str
