# pylint: skip-file

from dataclasses import dataclass
from datetime import date


@dataclass
class Participation:
    uuid: str
    registration: str
    project: str
    initial_date: date
    final_date: date
