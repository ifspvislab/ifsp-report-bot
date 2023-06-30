"""
This file contains a Python class named LogData.

Class:
    LogData: Manages log creation.
"""
import csv
import os


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

    def log_file_validation(
        self,
        file: str = "D:/Faculdade/VisLab/ifsp-report-bot/src/bot/cogs/log.pdf",
        limit_in_bytes: int = 26214400,
    ) -> bool:
        """
        Validates the size of a file.

        :param file: File to be validated.
        :type file: str
        :param limit_in_bytes: Maximum file size in bytes.
        :type limit_in_bytes: int
        :return: True if the file size exceeds the limit, False otherwise.
        :rtype: bool
        """

        file_size = os.path.getsize(file)
        if file_size < limit_in_bytes:
            return True
        return False
