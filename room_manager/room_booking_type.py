from dataclasses import dataclass


@dataclass
class RoomBookingTypes:
    instant = "Instant Booking"
    scheduled = "Scheduled Booking"