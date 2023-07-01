"""
services
=======

This package provides services for managing student data.

Modules
-------
.. autosummary::
    :toctree: generated/

    member_service
    student_service

Usage
-----

Import specific modules from the package:

.. code-block:: python

    from services import MemberService, StudentService

Use the imported modules to manage student data.

"""
import settings
from data.member_data import MemberData

logger = settings.logging.getLogger(__name__)

# pylint: disable=too-few-public-methods
class MemberService:
    """Class for managing member data.

    Args:
        member_data (MemberData): An instance of MemberData class for accessing member data.

    Attributes:
        member_data (MemberData): An instance of MemberData class for accessing member data.
    """

    def __init__(self, member_data: MemberData):
        self.member_data = member_data
        self.database = self.member_data.load_members()

    def find_member_by_type(self, attr_type, value):
        """
        Find a member in the database based on the specified attribute type and value.

        Args:
            attr_type (str): The attribute type to be checked.
            value: The value of the attribute to be matched.

        Returns:
            The member object if found, None otherwise.
        """
        for member in self.database:
            if getattr(member, attr_type) == value:
                return member

        return None