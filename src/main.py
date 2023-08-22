import time
import uuid
from logging.config import dictConfig

import uvicorn
from fastapi import Depends, FastAPI

from starlette.requests import Request

from src.app.utils.auto_discovery_util import AutoClassDiscoveryUtil
from src.app.dependencies import auth_dependency
import src.app.internal.admin
from src.app import controllers
import src.app.controllers.users
import src.app.controllers.items
import src.app.controllers.login
import src.app.controllers.signup

from src.app.entities import item, user
from src.app.internal.database import engine
import logging
from os import path

from src.app.searching import child_class
from src.app.searching.BaseClass import BaseClass

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.config')

item.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = str(uuid.uuid4())
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


app.include_router(src.app.controllers.users.router)
app.include_router(src.app.controllers.items.router)
app.include_router(src.app.controllers.login.app)
app.include_router(src.app.controllers.signup.router)
# app.include_router(
#     src.app.internal.admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(src.app.dependencies.dependencies.get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    logger.info("This is root")
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

