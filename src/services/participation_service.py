# pylint: skip-file

from datetime import datetime

from data import Participation


class ParticipationService:
    def find_participations_by_type(
        self, attr_type, value
    ) -> list[Participation] | None:

        return [
            Participation(
                "abc",
                "123",
                "aaaaa",
                datetime.now(),
                datetime(year=2050, month=8, day=15),
            ),
            Participation(
                "nnnnnnnnnn",
                "ppppppp",
                "ggggggggg",
                datetime.now(),
                datetime(year=2040, month=2, day=5),
            ),
        ]
