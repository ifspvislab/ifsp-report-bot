# pylint: skip-file

from datetime import datetime

from data import Project


class ProjectService:
    def find_project_by_type(self, attr_type, value):
        database = [
            Project(
                "asdqsweq",
                "Domingos Latorre",
                1111997040906469426,
                "VisLab: Laboratório de Visão Computacional",
                datetime(2023, 5, 2).date(),
                datetime(2023, 12, 15).date(),
            ),
            Project(
                "bcaeq",
                "Sabados Latorre",
                111199704090646942,
                "CodeLabs",
                datetime(2023, 7, 12).date(),
                datetime(2023, 11, 10).date(),
            ),
        ]
        for project in database:
            if getattr(project, attr_type) == value:
                return project
        return None
