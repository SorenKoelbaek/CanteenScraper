from fastapi import FastAPI, status
from routers import menu


app = FastAPI(
    title="Lego Menu Backend",
    description="",
    version="0.1.0",
    #docs_url=None,
    #redoc_url=None
)

app.include_router(menu.router)