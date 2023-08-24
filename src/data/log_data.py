"""
This file contains a Python class named LogData.

Class:
    LogData: Manages log creation.
"""

import csv
import os
from dataclasses import dataclass


@dataclass
class Log:
    """
    Data class to represent a log entry.

    Attributes:
    project_id (str): The ID of the associated project.
    registration (str): The registration information.
    discord_id (int): The Discord ID of the log creator.
    date (str): The date of the log entry.
    action (str): The action or description of the log.
    """

    project_id: str
    registration: str
    discord_id: int
    date: str
    action: str


class LogData:
    """
    Class for log management and member ID validation.
    """

    logs_file_path = "assets/data/logs.csv"

    def _row_to_log(self, row: str) -> dict:
        """
        Converts a row from the logs.csv file into a Log object.

        Args:
        - row: A row from the logs.csv file.

        Returns:
        - A dictionary representing a Log object.
        """
        fields = [field.strip() for field in row.split(sep=",")]
        action = ",".join(fields[4:])
        log = Log(fields[0], fields[1], int(fields[2]), fields[3], str(action))
        return log

    def load_logs(self) -> list[Log]:
        """
        Load log entries from the logs.csv file.

        Returns:
            list[Log]: A list of Log objects representing the log entries.
        """

        if not os.path.exists(self.logs_file_path):
            # pylint: disable=unused-variable
            with open(self.logs_file_path, "w", encoding="utf-8") as new_file:
                pass

        with open(self.logs_file_path, "r", encoding="utf-8") as file:
            logs = []
            for row in file:
                logs.append(self._row_to_log(row))
            return logs

    def add_log(self, log: Log) -> None:
        """
        Adds a log entry to the logs.csv file.

        Args:
        - log: A object containing the log data in the order
        [
            project_id,
            registration,
            discord_id,
            date,
            action
        ].
        """
        log_list = [
            log.project_id,
            log.registration,
            log.discord_id,
            log.date,
            log.action,
        ]
        with open(self.logs_file_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(log_list)
