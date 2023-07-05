# pylint: skip-file

from data import Coordinator


class CoordinatorService:
    def find_coordinator_by_type(self, attr_type, value):
        return Coordinator(
            "321", "SP54321X", 123151341, "Domingos LaTorre", "domingo.torre@gmail.com"
        )
