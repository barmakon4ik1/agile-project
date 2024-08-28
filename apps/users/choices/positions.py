from enum import Enum


class Positions(Enum):
    CEO = "CEO"
    CTO = "CTO"
    DESIGNER = "Designer"
    PRODUCT_OWNER = "Product Owner"
    PROJECT_OWNER = "Project Owner"
    PROGRAMMER = "Programmer"
    PROJECT_MANAGER = "Project Manager"
    QA = "QA"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]
