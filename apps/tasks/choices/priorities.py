from enum import Enum


class Priority(Enum):
    VERY_LOW = (1, 'Very Low')
    LOW = (2, 'Low')
    MEDIUM = (3, 'Medium')
    HIGH = (4, 'High')
    CRITICAL = (5, 'Critical')

    @classmethod
    def choices(cls):
        return [(key.value[0], key.value[1]) for key in cls]

    def __getitem__(self, item):
        return self.value[item]
