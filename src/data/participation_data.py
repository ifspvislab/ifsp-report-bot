# pylint: skip-file

from dataclasses import dataclass
from datetime import date


@dataclass
class Participation:
    participation_id: str
    registration: str
    project_id: str
    initial_date: date
    final_date: date