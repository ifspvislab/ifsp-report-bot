"""
Module to help with professor data.
"""

from data import _load_professors


class ProfessorService:
    """
    Service class to manage professor data.
    """

    def __init__(self) -> None:
        self.database = []

    def find_professor_by_discord_id(self, discord_id=int):
        """
        Defines professor by the discord ID.
        """
        if not self.database:
            self.database = _load_professors()

        for professor in self.database:
            if professor["discord_id"] == discord_id:
                return professor

        return None
