from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
import routers.pages
import routers.scores
import routers.utils
import time, os

os.environ['TZ'] = 'America/Bahia'
time.tzset()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

api = APIRouter(prefix="/api/v1")

app.include_router(routers.pages.router)
app.include_router(routers.scores.router)
app.include_router(routers.utils.router)

@api.get("/", tags=["test"])
async def hello():
    return {"message": "Hello World"}

