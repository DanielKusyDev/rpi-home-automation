from typing import List, Optional

from app.core.entities import Model, PaginatedResponse


class PlantInput(Model):
    name: str
    description: Optional[str]
    encoded_image: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Meyer Lemon",
                "description": "Lemon brought from England during the summer trip",
                "encoded_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYVFRgVF...",
            }
        }


class Plant(Model):
    id: int
    name: str
    description: Optional[str]
    image: Optional[str]
    sensors: Optional[str]


class PlantList(PaginatedResponse):
    results: List[Plant]
