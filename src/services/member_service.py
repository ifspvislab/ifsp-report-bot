"""
member_service
===============

This module provides a function for managing member data 

Function:
    - MemberService: Service class for managing member data
    - _check_campus: Verify fields standards
"""

from validate_email_address import validate_email
from data import load_members


def verify_standards(prontuario, email, discord_id) -> str:
    """
    Verifies the standards of the member's properties.

    Args:
        member: The member containing member properties.
    """
    _stats = []
    for error in _check_fields(prontuario, email, discord_id):
        _stats.append(error)
    for members in load_members():
        if prontuario.upper() == members["prontuario"]:
            _stats.append("Prontuario já cadastrado")

    if not _stats:
        _stats.append("Membro cadastrado com sucesso.")
    else:
        _stats.append("Infelismente não foi possivel cadastrar.")

    return _stats


def _check_fields(prontuario, email, discord_id):
    """
    Verify fields standards
    """
    _stats = []
    if not (
        prontuario[:1].isalpha()
        and prontuario[2:-2].isnumeric()
        and prontuario[-1].isalnum()
        and len(prontuario) == 9
    ):
        _stats.append("Prontuario incorreto")

    if not validate_email(email):
        _stats.append("email inválido")

    if not discord_id.isnumeric():
        _stats.append("discord_id inválido")

    return _stats
