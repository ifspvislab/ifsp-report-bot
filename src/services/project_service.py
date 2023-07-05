# pylint: skip-file

from data import Project
from datetime import datetime

class ProjectService:
    def find_project_by_type(self, attr_type, value) -> Project:
        return Project(
                "abc", 
                "Domingos Latorre", 
                1111997040906469426, 
                "VisLab: Laboratório de Visão Computacional", 
                datetime(2023, 5, 2).date(), 
                datetime(2023, 12, 15).date()
            )
