# pylint: skip-file

from dataclasses import dataclass


@dataclass
class Project:
    project_id: str
    coordenador: str
    discord_server_id: int
    titulo: str
    data_inicio: int
    data_fim: int
