from django.db import models
from django.db import transaction


class Building(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


    def update_floors(self, floors: list) -> bool:
        try:
            unique_floor_names = list(dict.fromkeys(floors))

            with transaction.atomic():
                # Update the actual_floor values if the floors exist, or create
                # new floors if they don't
                for idx, floor_name in enumerate(unique_floor_names):
                    floor = self.floors.filter(name__exact=floor_name).first()

                    if floor is None:
                        floor = Floor(building=self, name=floor_name, actual_floor=idx)
                    else:
                        floor.actual_floor = idx
                    
                    floor.save()
                
                # Then remove floors that are not in the provided list.
                for floor in self.floors.all():
                    if floor.name not in unique_floor_names:
                        floor.delete()
                
            return True
        except Exception as e:
            print(e)
            return False


class Floor(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE, related_name='floors')
    name = models.CharField(max_length=150)

    # The index of the floor in the floors array.
    # Will be equivalent to the actual floor and will be used for floor difference calculations,
    # as opposed to the floor names, which may be integers, but may also be e.g. "Underground-1".
    actual_floor = models.IntegerField()

    def __str__(self) -> str:
        building_name = self.building.name if self.building else ''
        return f"{building_name} | Floor: {self.name}"