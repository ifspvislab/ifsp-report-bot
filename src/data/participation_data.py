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
    prontuario: str
    project: str
    data_inicio: date
    data_final: date


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
        data.participation_id = fields[0]
        data.prontuario = fields[1]
        data.project = fields[2]
        data.data_inicio = datetime.strptime(fields[3], "%d/%m/%Y").date()
        data.data_final = datetime.strptime(fields[4], "%d/%m/%Y").date()

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

    def add_participation(self, participation: Participation):
        """
        Add the participations to the database.

        :param participation: the participation dataclass.
        :type participation: Dataclass.
        """
        initial_date = datetime.strftime(participation.data_inicio, "%d/%m/%Y")
        final_date = datetime.strftime(participation.data_final, "%d/%m/%Y")
        with open(
            "assets/data/participations.csv", "a", encoding="UTF-8"
        ) as participation_data:
            participation_data.write(
                f"{participation.participation_id},{participation.prontuario},"
                + f"{participation.project},{initial_date},{final_date}\n"
            )
        participation_data.close()
