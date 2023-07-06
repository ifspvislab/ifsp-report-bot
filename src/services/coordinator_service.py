# pylint: skip-file

from data import Coordinator


class CoordinatorService:
    def find_coordinator_by_type(self, attr_type, value):
        database = [
            Coordinator(
                "123",
                "SP54321X",
                123151341,
                "Domingos LaTorre",
                "domingo.torre@gmail.com",
            ),
            Coordinator(
                "321", "SP12345X", 5432542352, "Sabados LaTorre", "sabados@gmail.com"
            ),
        ]
        for coordinator in database:
            if getattr(coordinator, attr_type) == value:
                return coordinator

        return None
