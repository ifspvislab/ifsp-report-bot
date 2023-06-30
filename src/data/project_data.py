""" 
This module contains the definition of the 'Project' and 'ProjectData' classes,
which are used for managing project data.
Classes:
    Project: A class that represents a Project.
    ProjectData: A class for managing project data
"""

from dataclasses import dataclass


@dataclass
class Project:
    """ """

    project_id: str
    coordenador: str
    discord_server_id: int
    titulo: str
    data_inicio: int
    data_fim: int
