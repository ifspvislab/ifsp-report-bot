"""
:mod: member_data
=================

Module for managing member data stored in a CSV file.

Module Dependencies:
    - ``csv``: A module for working with CSV files.

Classes:
    - :class:`MemberData`: Class for managing member data.

"""


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

    # pylint: disable=duplicate-code
    def _row_to_member(self, row: str) -> dict:
        """
        .. method:: _row_to_member(row: str) -> dict

        Convert a row of member data to a dictionary.

        :param row: The row of member data.
        :type row: str
        :return: A dictionary representing the member.
        :rtype: dict
        """
        fields = [field.strip() for field in row.split(sep=",")]

        return {
            "prontuario": fields[0],
            "discord_id": int(fields[1]),
            "name": fields[2],
            "email": fields[3],
        }

    def add_member(self, member):
        """
        .. method:: add_member(member)

        Add project member data to the CSV file.

        :param member: An instance of the Member class representing the member.
        :type member: Member

        """
        with open("assets/data/members.csv", "a", encoding="UTF-8") as member_data:
            member_data.write(
                f"{member.prontuario}, {member.discord_id}, {member.name}, {member.email}\n"
            )

    def load_members(self) -> list[dict]:
        """
        .. method:: load_members() -> list[dict]

        Load members from the CSV file.

        :return: A list of member dictionaries.
        :rtype: list[dict]

        """
        with open("assets/data/members.csv", "r", encoding="utf-8") as file:
            members = []
            for row in file:
                members.append(self._row_to_member(row))
            return members
