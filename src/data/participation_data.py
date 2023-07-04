""" 
Participation Data
"""

from dataclasses import dataclass


@dataclass
class Participation:
    """
    Dataclass containing all the participation infos.
    """

    participation_id: str
    prontuario: str
    project: str
    data_inicio: str
    data_final: str


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
        data.data_inicio = fields[3]
        data.data_final = fields[4]

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
        with open(
            "assets/data/participations.csv", "a", encoding="UTF-8"
        ) as participation_data:
            participation_data.write(
                f"{participation.participation_id},{participation.prontuario},"
                + f"{participation.project},{participation.data_inicio},{participation.data_final}"
            )
        participation_data.close()
