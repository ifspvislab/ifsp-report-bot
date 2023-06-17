"""
:mod: coordinator_data
======================

Module for managing coordinator data stored in a CSV file.

Module Dependencies:
    - ``csv``: A module for working with CSV files.

Classes:
    - :class:`CoordinatorData`: Class for managing coordinator data.

Usage:
    1. Import the module:

        .. code-block:: python

            import coordinator_data

    2. Create an instance of the CoordinatorData class:

        .. code-block:: python

            coordinator = coordinator_data.CoordinatorData()

    3. Use the methods of the CoordinatorData class to manage coordinator data.
"""
# pylint: disable=too-few-public-methods
class CoordinatorData:
    """
    :class: CoordinatorData
    ======================

    Class for managing coordinator data stored in a CSV file.

    Module Dependencies:
        - ``csv``: A module for working with CSV files.

    Methods:
        - ``__init__()``: Initialize the CoordinatorData class.
        - ``_row_to_coordinator(row: str) -> dict``: Convert a row of
        coordinator data to a dictionary.
        - ``load_coordinator() -> list[dict]``: Load coordinator from the CSV file.

    """

    def _row_to_coordinator(self, row: str) -> dict:
        """
        .. method:: _row_to_coordinator(row: str) -> dict

        Convert a row of coordinator data to a dictionary.

        :param row: The row of coordinator data.
        :type row: str
        :return: A dictionary representing the coordinator.
        :rtype: dict
        """
        fields = [field.strip() for field in row.split(sep=",")]
        return {
            "prontuario": fields[0],
            "discord_id": int(fields[1]),
            "name": fields[2],
            "email": fields[3],
        }

    def load_coordinator(self) -> list[dict]:
        """
        .. method:: load_coordinator() -> list[dict]

        Load coordinator from the CSV file.

        :return: A list of coordinator dictionaries.
        :rtype: list[dict]
        """
        with open("assets/data/coordinators.csv", "r", encoding="utf-8") as file:
            coordinator = []
            for row in file:
                coordinator.append(self._row_to_coordinator(row))
            return coordinator
