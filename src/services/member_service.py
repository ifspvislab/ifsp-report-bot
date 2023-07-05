# pylint: skip-file

from data import Member


class MemberService:
    def find_member_by_type(self, attr_type, value) -> Member | None:
        database = [
            Member("123", "SPXXXXXXX", 733007663356444742, "Gabriel", "aaaa@aaaa.com")
        ]
        for member in database:
            if getattr(member, attr_type) == value:
                return member
        return None
