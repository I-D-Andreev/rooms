from dataclasses import dataclass


@dataclass
class UserGroups():
    admins = "admins"
    users = "users"
    rooms = "rooms"

    @staticmethod
    def as_list():
        return [UserGroups.admins, UserGroups.users, UserGroups.rooms]
