from dataclasses import dataclass

@dataclass
class MeetingDistanceTypes:
    same_floor = "Same Floor"
    same_building = "Same Building"
    number_floors = "Specific Number Of Floors"
    near_buildings = "This And Nearby Buildings"

    @staticmethod
    def as_list():
        return [MeetingDistanceTypes.same_floor, MeetingDistanceTypes.same_building,
                MeetingDistanceTypes.number_floors, MeetingDistanceTypes.near_buildings]

    
    @staticmethod
    def as_choice_list():
        return[(mdt, mdt) for mdt in MeetingDistanceTypes.as_list()]


