#pylint: skip-file

from dataclasses import dataclass

@dataclass
class Coordinator:
    coord_id: str
    registration: str
    discord_id: int
    name: str
    email: str
