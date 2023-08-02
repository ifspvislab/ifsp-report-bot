"""Services for administrator"""
from settings import get_admin_id

ID_ADMIN = int(get_admin_id())

def is_admin(user_id):
    """Check if it's the administrator doing the command by the discord id user"""
    if user_id == ID_ADMIN:
        return True
    return False
