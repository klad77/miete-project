from enum import Enum


class Positions(Enum):
    ADMIN = "Admin"
    OWNER = "Owner"
    USER = "User"


    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]
