"""
This file contains a Python class named LogData.

Class:
    LogData: Manages log creation.
"""
import csv


class LogData:
    """
    Class for log management and member ID validation.
    """

    def create_logs(self, data_list: list) -> None:
        """
        Appends data_list to "logs.csv" file.

        Parameters:
            - data_list: List of data to be written.

        Returns:
            None
        """
        with open("assets/data/logs.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_list)
