"""
This file contains a Python class named LogData.

Class:
    LogData: Manages log creation.
"""

import csv
from dataclasses import dataclass


@dataclass
class Log:
    """
    Data class to represent a log entry.

    Attributes:
    - discord_id: The Discord ID of the log creator.
    - date: The date of the log entry.
    - action: The action or description of the log.
    """

    discord_id: int
    date: str
    action: str


class LogData:
    """
    Class for log management and member ID validation.
    """

    def _row_to_log(self, row: str) -> dict:
        """
        Converts a row from the logs.csv file into a Log object.

        Args:
        - row: A row from the logs.csv file.

        Returns:
        - A dictionary representing a Log object.
        """
        fields = [field.strip() for field in row.split(sep=",")]
        action = ",".join(fields[2:])
        log = Log(int(fields[0]), fields[1], str(action))
        return log

    def load_logs(self) -> list[dict]:
        """
        Loads log entries from the logs.csv file.

        Returns:
        - A list of dictionaries representing the log entries.
        """
        with open("assets/data/logs.csv", "r", encoding="utf-8") as file:
            logs = []
            for row in file:
                logs.append(self._row_to_log(row))
            return logs

    def add_log(self, log: Log) -> None:
        """
        Adds a log entry to the logs.csv file.

        Args:
        - log: A object containing the log data in the order [discord_id, date, action].
        """
        log_list = [log.discord_id, log.date, log.action]
        with open("assets/data/logs.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(log_list)
