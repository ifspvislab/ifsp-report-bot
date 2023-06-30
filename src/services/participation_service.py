# pylint: skip-file

"""Service regarding input issues"""

from datetime import datetime

from data import Participation


class ParticipationService:
    """
    A service for managing participations.
    """

    def find_participation_by_discord_id(
        self, discord_id: int
    ) -> list[Participation] | None:
        """
        Find a participation in the database with the user discord ID.
        :param discord_id: The discord ID of the user.
        :return: The participation of the student.
        :rtype: Dataclass
        """

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
