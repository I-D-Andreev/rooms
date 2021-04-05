from dataclasses import dataclass


@dataclass
class UserTypes:
    admin = "admin"
    user = "user"
    room = "room"

    @staticmethod
    def as_list():
        return [UserTypes.admin, UserTypes.user, UserTypes.room]

    @staticmethod
    def as_choice_list():
        return [(t, t) for t in UserTypes.as_list()]

    @staticmethod
    def user_admin_choice_list():
        return [(t,t) for t in [UserTypes.user, UserTypes.admin]]
