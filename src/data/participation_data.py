""" 
Participation Data
"""

import os
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

    participations_file_path = "assets/data/participations.csv"

    def row_to_participation(self, row: str) -> Participation:
        """
        Converts a row of participation into a dataclass.

        :param row: The row of participation data.
        :type row: str
        :return: A dataclass representing the participation.
        :rtype: Dataclass.
        """
        fields = [field.strip() for field in row.split(sep=",")]
        data = Participation(
            participation_id=fields[0],
            registration=fields[1],
            project_id=fields[2],
            initial_date=datetime.strptime(fields[3], "%d/%m/%Y").date(),
            final_date=datetime.strptime(fields[4], "%d/%m/%Y").date(),
        )

        return data

    def load_participations(self) -> list[Participation]:
        """
        Load the participations from the database.

        :return: A list of participations dataclasses.
        :rtype: list.
        """

        if not os.path.exists(self.participations_file_path):
            # pylint: disable=unused-variable
            with open(self.participations_file_path, "w", encoding="utf-8") as new_file:
                pass

        participations = []
        with open(self.participations_file_path, "r", encoding="utf-8") as file:
            for row in file:
                participations.append(self.row_to_participation(row))
        return participations

    def add_participation(self, participation: Participation):
        """
        Add the participations to the database.

        :param participation: the participation dataclass.
        :type participation: Dataclass.
        """
        initial_date = datetime.strftime(participation.initial_date, "%d/%m/%Y")
        final_date = datetime.strftime(participation.final_date, "%d/%m/%Y")
        with open(
            self.participations_file_path, "a", encoding="UTF-8"
        ) as participation_data:
            participation_data.write(
                f"{participation.participation_id},{participation.registration},"
                + f"{participation.project_id},{initial_date},{final_date}\n"
            )
        participation_data.close()
