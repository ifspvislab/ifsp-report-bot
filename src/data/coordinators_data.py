"""
Professors Data
"""

from dataclasses import dataclass


@dataclass
class Coordinator:
    """
    Dataclass containing the professors data.
    """

    uuid: str
    discord_id: str
    name: str


class CoordinatorData:
    """
    Class for managing coordinator data.
    """

    def __init__(self) -> None:
        self.coordinator_data = CoordinatorData

    def _row_to_coordinator(self, row: str) -> Coordinator:
        fields = [field.strip() for field in row.split(sep=",")]
        data = Coordinator
        data.uuid = fields[0]
        data.discord_id = int(fields[1])
        data.name = fields[2]
        return Coordinator

    def load_coordinators(self) -> list[Coordinator]:
        """
        Loads coordinators from the CSV file.

        :return: A list of the professors dataclasses.
        :rtype: list
        """

        with open("assets/data/coordinators.csv", "r", encoding="utf-8") as file:
            coordinators = []
            for row in file:
                coordinators.append(self._row_to_coordinator(row))
        return coordinators

    def find_coordinator_by_discord_id(self, discord_id: int) -> Coordinator | None:
        """
        Determines if the user is a professor by his discord ID.

        :param discord_id: User's discord ID.
        :type discord_id: int
        :return: Professor data or None
        :rtype: Dataclass or None

        """

        database = []

        if not database:
            database = self.load_coordinators()

        for coordinator in database:
            if coordinator.discord_id == discord_id:
                return Coordinator

        return None
