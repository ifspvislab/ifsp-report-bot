"""
:mod: member_data
=================

Module for managing member data stored in a CSV file.

Module Dependencies:
    - ``csv``: A module for working with CSV files.

Classes:
    - :class:`MemberData`: Class for managing member data.

"""

import os
from dataclasses import dataclass


@dataclass
class Member:
    """Class representing a member.

    Attributes:
        member_id(str): The ID of the member.
        registration (str): The registration of the member.
        discord_id (int): The Discord ID of the member.
        name (str): The name of the member.
        email (str): The email address of the member.
    """

    member_id: str
    registration: str
    discord_id: int
    name: str
    email: str


class MemberData:
    """
    :class: MemberData
    ==================

    Class for managing member data stored in a CSV file.

    Module Dependencies:
        - ``csv``: A module for working with CSV files.

    Methods:
        - ``_row_to_member(row: str) -> dict``: Convert a row of member data to a dictionary.
        - ``add_member(member)``: Add project member data to the CSV file.
        - ``load_members() -> list[dict]``: Load members from the CSV file.
    """

    members_file_path = "assets/data/members.csv"

    # pylint: disable=duplicate-code
    def _row_to_member(self, row: str) -> Member:
        """
        .. method:: _row_to_member(row: str) -> dict

        Convert a row of member data to a dictionary.

        :param row: The row of member data.
        :type row: str
        :return: A dictionary representing the member.
        :rtype: dict
        """
        fields = [field.strip() for field in row.split(sep=",")]
        member = Member(fields[0], fields[1], int(fields[2]), fields[3], fields[4])
        return member

    def add_member(self, member: Member):
        """
        .. method:: add_member(member)

        Add project member data to the CSV file.

        :param member: An instance of the Member class representing the member.
        :type member: Member

        """
        with open(self.members_file_path, "a", encoding="UTF-8") as member_data:
            member_data.write(
                f"{member.member_id},{member.registration},"
                + f"{member.discord_id},{member.name},{member.email}\n"
            )

    def load_members(self) -> list[Member]:
        """
        .. method:: load_members() -> list[dict]

        Load members from the CSV file.

        :return: A list of member dictionaries.
        :rtype: list[dict]

        """

        if not os.path.exists(self.members_file_path):
            # pylint: disable=unused-variable
            with open(self.members_file_path, "w", encoding="utf-8") as new_file:
                pass

        with open(self.members_file_path, "r", encoding="utf-8") as file:
            members = []
            for row in file:
                members.append(self._row_to_member(row))
            return members
