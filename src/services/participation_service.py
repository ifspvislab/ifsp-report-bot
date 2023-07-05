"""
=====================
Participation Service
=====================

This package provides services for managing participation data. 
"""

from data.member_data import MemberData
from data.participation_data import Participation, ParticipationData


# pylint: disable=too-few-public-methods
class ParticipationService:
    """
    Class for managing participation data.
    Args:
        participation_data (ParticipationData): An instance of ParticipationData class for
    accessing participation data.
        member_data (MemberData): An instance of MemberData class for accessing member data.
        project_service (ProjectService): An instance of ProjectService for acessing project data.
        member_service (MemberService): An instance of MemberService for acessing member data.
    Attributes:
        participation_data (ParticipationData): An instance of ParticipationData class for
    accessing participation data.
        member_data (MemberData): An instance of MemberData class for accessing member data.
        project_service (ProjectService): An instance of ProjectService for acessing project data.
        member_service (MemberService): An instance of MemberService for acessing member data.
    """

    def __init__(
        self,
        participation_data: ParticipationData,
        member_data: MemberData,
    ) -> None:
        """ """
        self.member_data = member_data
        self.participation_data = participation_data

        self.database = self.participation_data.load_participations()
        self.members = self.member_data.load_members()

    def find_participations_by_type(
        self, attr_type, value
    ) -> list[Participation] | None:
        """
        Find all the participations in the database based on the specified attribute type and value.
        Args:
            attr_type (str): The attribute type to be checked.
            value: The value of the attribute to be matched.
        Returns:
            A participations list if found, None otherwise.
        """
        participations = []
        for participation in self.database:
            if getattr(participation, attr_type) == value:
                participations.append(participation)
        if participations:
            return participations
        return None
