# pylint: skip-file

from data import Member


class MemberService:
    def find_member_by_type(self, attr_type, value) -> Member:
        return Member(
            "123", "SPXXXXXXX", 733007663356444742, "Gabriel", "aaaa@aaaa.com"
        )
