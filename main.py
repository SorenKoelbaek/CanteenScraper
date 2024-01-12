from fastapi import FastAPI, status
from routers import menu
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Lego Menu Backend",
    description="",
    version="0.1.0",
    #docs_url=None,
    #redoc_url=None
)

origins = [
    "http://localhost:8000",
    "http://canteen.sorenkoelbaek.dk",
    "https://canteen.sorenkoelbaek.dk",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu.router)