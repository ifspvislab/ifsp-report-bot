# pylint: skip-file

from datetime import datetime

from data import Participation


class ParticipationService:
    def find_participation_by_type(
        self,
        attr_type,
        value,
    ):
        """."""
        database = [
            Participation(
                "abc",
                "SPXXXXXX",
                "asdqsweq",
                datetime(2023, 5, 2).date(),
                datetime(2023, 12, 15).date(),
            ),
            Participation(
                "cba",
                "SPXXXXXX",
                "bcaeq",
                datetime(2023, 7, 3).date(),
                datetime(2023, 12, 30).date(),
            ),
        ]

        participations = []
        for participation in database:
            if getattr(participation, attr_type) == value:
                participations.append(participation)
        if participations:
            return participations

        return None
