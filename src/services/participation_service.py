# pylint: skip-file

from datetime import datetime

from data import Participation


class ParticipationService:
    def find_participation_by_type(
        self,
        attr_type,
        value,
    ) -> list[Participation] | None:

        return [
            Participation(
                "abc",
                "SPXXXXXXX",
                "aabbcc",
                datetime(2023, 5, 2).date(),
                datetime(year=2023, month=12, day=15).date(),
            ),
            Participation(
                "cba",
                "SPXXXXXX",
                "ccbbaa",
                datetime(2023, 7, 3).date(),
                datetime(2023, 12, 30).date(),
            ),
        ]
