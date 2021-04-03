from dataclasses import dataclass


@dataclass
class RoomBookingTypes:
    instant = "Instant Booking"
    scheduled = "Scheduled Booking"

    @staticmethod
    def as_list():
        return [RoomBookingTypes.instant, RoomBookingTypes.scheduled]

    @staticmethod
    def as_choice_list():
        return [(t,t) for t in RoomBookingTypes.as_list()]
