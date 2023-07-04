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
    """
    A class that represents a coordinator.

    Attributes:
        registration (str): The coordinator's registration.
        discord_id (int): The coordinator's Discord ID.
        name (str): The coordinator's name.
        email (str): The coordinator's email.
    """

    coord_id: str
    registration: str
    discord_id: int
    name: str
    email: str


class CoordinatorData:
    """
    A class for managing coordinator data.

    Methods
    -------
    _row_to_coordinator(row: str) -> dict
        Converts a row of data from the coordinators.csv file into a dictionary format.

    load_coordinators() -> list[dict]
        Loads coordinator data from the coordinators.csv file and returns a list of dictionaries.

    add_coordinator(registration, name, email, discord_id)
        Adds a new coordinator to the coordinators.csv file.
    """

    def _row_to_coordinator(self, row: str) -> dict:
        """
        Converts a row of data from the coordinators.csv file into a dictionary.

        :param row: The row of data representing a coordinator.
        :type row: str
        :return: A dictionary representing the coordinator's registration, 
        discord_id, name and email.
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

    def add_coordinator(self, coord: Coordinator) -> None:
        """
        Add coordinator data to the CVS file

        :param registration: coordinator registration
        :type registration: str
        :param name: coordinator name
        :type name: str
        :param email: coordinator email
        :type email: str
        :param discord_id: coordinator discord_id
        :type discord_id: int
        """

        with open(
            "assets/data/coordinators.csv", "a", encoding="UTF-8"
        ) as coordinator_data:
            coordinator_data.write(
                f"{coord.coord_id}, {coord.registration},"
                + f" {coord.discord_id}, {coord.name}, {coord.email}\n"
            )
