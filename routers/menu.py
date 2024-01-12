import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from models.appmodels import *
from dependencies.scraper import getWeekMenu, locationvalidator
from typing import Union

router = APIRouter(
    prefix="/menu",
    tags=["Menues"],
    responses={404: {"description": "Not found"}},
)



@router.get("/", response_model=list[Menu])
async def get_menus(
        lang: str = "en",
        location: str = "kantine-oestergade"
    ):

    if not locationvalidator(location):
        raise (HTTPException(status_code=204, detail="location is malformed"))

    result_menus = []
    menus = getWeekMenu(location)
    for menu in menus:
        menu.dishes = [d for d in menu.dishes if d.lang == lang]
        result_menus.append(menu)
    return result_menus


@router.get("/today", response_model=Menu)
async def get_menu_today(
    lang: str = "en",
    location: str = "kantine-oestergade"
    ):
    menus = getWeekMenu(location)
    current_dateTime = datetime.datetime.now()

    menu = [x for x in menus if x.day == datetime.datetime(current_dateTime.year, current_dateTime.month, current_dateTime.day)][0]
    menu.dishes = [d for d in menu.dishes if d.lang == lang]

    return menu



@router.get("/locations", response_model=list[str])
async def get_locations(
    ):

    return ['multihuset', "havremarken", "kl-verblomsten", "aastvej", "midtown", "kornmarken", "kantine-oestergade"]

