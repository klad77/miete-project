from enum import Enum


class Properties(Enum):
    APARTMENT = "Apartment"
    HOUSE = "House"
    ROOM = "Room"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]
