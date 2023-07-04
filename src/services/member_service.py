# pylint: skip-file

from data.member_data import Member


class MemberService:
    def find_member_by_type(self, attr_type, value) -> Member:
        return Member("123", "blabla", 454379770982039575, "gui", "aaaa@aaaa.com")
