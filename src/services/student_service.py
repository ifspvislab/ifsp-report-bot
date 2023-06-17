"""
student_service
=======================

This module provides the StudentService class for managing student data.

Classes:
    - StudentService: Service class for managing student data.

"""

from data import StudentData


# pylint: disable-next=too-few-public-methods
class StudentService:
    """
    Service class for managing student data.

    Methods:
        - __init__(): Initialize the StudentService object.
        - find_student_by_discord_id(discord_id: int) -> dict | None: Find a student by
        Discord ID in the student database.

    Attributes:
        - database: List to store student data.
    """

    def __init__(self) -> None:
        """
        Initialize the StudentService object.

        Sets up the initial state by creating an empty `database` list to store student data.
        """
        self.database = []

    def find_student_by_discord_id(self, discord_id: int) -> dict | None:
        """
        Find a student by Discord ID in the student database.

        If the student data has not been loaded yet, it will be loaded from the file
        using the `load_students()` function and stored in the `self.database` attribute.
        Subsequent calls to this method will directly search for the student in the cached
        data, avoiding redundant file I/O operations.

        :param discord_id: The Discord ID of the student to find.
        :type discord_id: int
        :return: A dictionary representing the student if found, or None if not found.
        :rtype: dict | None
        """
        if not self.database:
            student_data = StudentData()
            self.database = student_data.load_students()

        for student in self.database:
            if student["discord_id"] == discord_id:
                return student

        return None
