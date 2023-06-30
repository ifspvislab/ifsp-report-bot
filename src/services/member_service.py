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

from data.member_data import Member


class MemberService:
    """Class for managing member data.
    Args:
        member_data (MemberData): An instance of MemberData class for accessing member data.
    Attributes:
        member_data (MemberData): An instance of MemberData class for accessing member data.
    """

    def find_member_by_type(self, attr_type, value) -> Member:
        """
        Find a member in the database based on the specified attribute type and value.
        Args:
            attr_type (str): The attribute type to be checked.
            value: The value of the attribute to be matched.
        Returns:
            The member object if found, None otherwise.
        """

        return Member("123", "blabla", 454379770982039575, "gui", "aaaa@aaaa.com")
