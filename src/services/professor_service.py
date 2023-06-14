from data import _load_professors


class ProfessorService:
    """
    Service class to manage professor data.
    """

    def __init__(self) -> None:
        self.database = []

    def find_professor_by_discord_id(self, discord_id=int):
        if not self.database:
            self.database = _load_professors()

        for coordinator in self.database:
            if coordinator["discord_id"] == discord_id:
                return coordinator

        return None
