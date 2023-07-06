# pylint: skip-file

import csv
from datetime import datetime

from data import Participation


class ParticipationService:
    def find_participation_by_type(
        self,
        attr_type,
        value,
    ):
        """ "."""
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

    def write_termination_date_in_participations(
        self, projects_id, guild_project_id, termination_date
    ):
        """
        Writes the termination date inserted by a member on
        participations.csv, overwriting the termination date associated
        with the member's participation

        Args:
            projects_id: The projects IDs associated with the member's
            participations.
            guild_project_id: The ID of the server where the request was
            made.
            termination_date: The termination date inserted by the member
        """
        participation_project_id = str()
        for project_id in projects_id:
            if project_id == guild_project_id:
                participation_project_id = project_id
        i = 0
        line = 0

        with open("assets/data/participations.csv", "r", encoding="UTF-8") as file:
            for row in file:
                if participation_project_id in row:
                    modified_lines = []
                    line = i
                    with open(
                        "assets/data/participations.csv",
                        "r",
                        encoding="UTF-8",
                    ) as file:
                        reader = csv.reader(file)
                        for row in reader:
                            modified_lines.append(row)

                    modified_lines[line][4] = termination_date.strftime("%d/%m/%Y")

                    with open(
                        "assets/data/participations.csv",
                        "w",
                        encoding="UTF-8",
                        newline="",
                    ) as file:
                        writer = csv.writer(file)
                        writer.writerows(modified_lines)
                i += 1
