# pylint: skip-file

from dataclasses import dataclass


@dataclass
class Member:
    member_id: str
    prontuario: str
    discord_id: int
    name: str
    email: str
