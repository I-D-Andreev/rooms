import builtins
from django.db import models
from django.db import transaction
from queue import Queue

class Building(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)

    close_buildings = models.ManyToManyField('self')

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

    def get_near_buildings(self):
        return [self] + list(self.close_buildings.all())


    def get_near_buildings_infer(self):
        q = Queue()
        near_buildings = set()

        q.put(self)

        while not q.empty():
            building = q.get()
            near_buildings.add(building)

            for b in list(building.close_buildings.all()):
                if b not in near_buildings:
                    q.put(b)

        return near_buildings

    def is_directly_nearby(self, building):
        return bool(building in self.close_buildings.all())

    @staticmethod
    def all_nearby_building_pairs_list(shouldInfer):
        nearby_buildings_list = []
        already_appeared = set()

        buildings = Building.objects.all()
        
        for building in buildings:
            close_buildings = building.get_near_buildings_infer() if shouldInfer else building.get_near_buildings()

            for close_building in close_buildings:
                if building.id != close_building.id \
                    and ((building.id, close_building.id) not in already_appeared) \
                    and ((close_building.id, building.id) not in already_appeared):
                    
                    already_appeared.add((building.id, close_building.id))
                    nearby_buildings_list.append((building, close_building, building.is_directly_nearby(close_building)))

        return nearby_buildings_list






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