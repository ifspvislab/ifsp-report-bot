# pylint: skip-file

from data.project_data import Project


class ProjectService:
    def find_project_by_type(self, attr_type, value) -> Project | None:
        return Project("aaaaa", "oooooo", 123132, "abba", 1, 2)
