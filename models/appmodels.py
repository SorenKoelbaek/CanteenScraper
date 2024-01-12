from pydantic import BaseModel
import datetime


class Dish(BaseModel):
    dish_type: str
    name: str
    lang: str


class Menu(BaseModel):
    day: datetime.datetime
    dishes: list[Dish]

