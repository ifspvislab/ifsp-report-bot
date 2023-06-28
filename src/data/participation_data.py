""" 
Participation Data
"""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Participation:
    """
    Dataclass containing all the participation infos.
    """

    uuid: str
    registration: str
    project: str
    initial_date: date
    final_date: date


class ParticipationData:
    """
    Class for managing participation data.
    """

    def __init__(self) -> None:
        pass

    def row_to_participation(self, row: str) -> Participation:
        """
        Converts a row of participation into a dataclass.

        :param row: The row of participation data.
        :type row: str
        :return: A dataclass representing the participation.
        :rtype: Dataclass.
        """
        data = Participation
        fields = [field.strip() for field in row.split(sep=",")]
        data.id = fields[0]
        data.registration = fields[1]
        data.project = fields[2]
        data.initial_date = datetime.strptime(fields[3, "%d/%m/%y"]).date()
        data.final_date = datetime.strptime(fields[4, "%d/%m/%y"]).date()

        return Participation

    def load_participations(self) -> list[Participation]:
        """
        Load the participations from the database.

        :return: A list of participations dataclasses.
        :rtype: list.
        """

        with open("assets/data/participations.csv", "r", encoding="utf-8") as file:
            participations = []
            for row in file:
                participations.append(self.row_to_participation(row))
        return participations
