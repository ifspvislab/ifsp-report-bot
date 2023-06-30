""" 
Participation Data
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Participation:
    """
    Dataclass containing all the participation infos.
    """

    uuid: str
    registration: str
    project: str
    initial_date: date
    final_date: date
