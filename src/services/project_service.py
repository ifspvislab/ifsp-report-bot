# pylint: skip-file

from datetime import date

from data.project_data import Project


class ProjectService:
    def find_project_by_type(self, attr_type, value) -> Project | None:
        return Project(
            "aaaaa", "oooooo", 123132, "abba", date(123, 11, 22), date(456, 10, 11)
        )
