"""

This module contains the definition of the `Coordinator` and `CoordinatorData` classes, 
which are used for managing coordinator data.

Classes:
    Coordinator: A class that represents a coordinator.
    CoordinatorData: A class for managing coordinator data.

"""

from dataclasses import dataclass


@dataclass
class Coordinator:
    coord_id: str
    prontuario: str
    discord_id: int
    nome: str
    email: str


class CoordinatorData:
    def _row_to_coordinator(self, row: str) -> dict:
        """
        Converts a row of data from the coordinators.csv file into a dictionary.

        :param row: The row of data representing a coordinator.
        :type row: str
        :return: A dictionary representing the coordinator's prontuario, discord_id, nome and email.
        :rtype: dict
        """

        fields = [field.strip() for field in row.split(sep=",")]
        coordinator = Coordinator(
            fields[0], fields[1], int(fields[2]), fields[3], fields[4]
        )
        return coordinator

    def load_coordinators(self) -> list[Coordinator]:
        """
        Load coordinator from the CSV file and return a list of dictionaries.

        :return: A list of dictionaries, where each dictionary represents a coordinator.
        :rtype: list[dict]
        """

        with open("assets/data/coordinators.csv", "r", encoding="utf-8") as file:
            coordinators = []
            for row in file:
                coordinators.append(self._row_to_coordinator(row))
            return coordinators

    def add_coordinator(self, coordinator: Coordinator) -> None:
        """
        Add coordinator data to the CVS file

        :param prontuario: coordinator prontuario
        :type prontuario: str
        :param nome: coordinator nome
        :type nome: str
        :param email: coordinator email
        :type email: str
        :param discord_id: coordinator discord_id
        :type discord_id: int
        """

        with open(
            "assets/data/coordinators.csv", "a", encoding="UTF-8"
        ) as coordinator_data:
            coordinator_data.write(
                f"{coord.coord_id}, {coord.prontuario}, {coord.discord_id}, {coord.nome}, {coord.email}\n"
            )
