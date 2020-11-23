from dataclasses import dataclass


@dataclass
class UserTypes:
    admins = "admin"
    users = "user"
    rooms = "room"

    @staticmethod
    def as_list():
        return [UserTypes.admins, UserTypes.users, UserTypes.rooms]

    @staticmethod
    def as_choice_list():
        return [(t, t) for t in UserTypes.as_list()]
