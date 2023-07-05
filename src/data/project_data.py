# pylint: skip-file

from dataclasses import dataclass
from datetime import date


@dataclass
class Project:
    project_id: str
    coordinator_id: str
    discord_server_id: int
    title: str
    start_date: date
    end_date: date
