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

    participation_id: str
    registration: str
    project_id: str
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
        fields = [field.strip() for field in row.split(sep=",")]
        participation = Participation(
            participation_id=fields[0],
            registration=fields[1],
            project_id=fields[2],
            initial_date=datetime.strptime(fields[3], "%d/%m/%Y").date(),
            final_date=datetime.strptime(fields[4], "%d/%m/%Y").date(),
        )
        return participation

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
