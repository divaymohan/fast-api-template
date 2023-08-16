from fastapi import Depends, FastAPI

import uvicorn
from src.app.dependencies import dependencies
import src.app.internal.admin
from src.app import controllers
import src.app.controllers.users
import src.app.controllers.items
from src.app.entities import item, user
from src.app.internal.database import engine

item.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(src.app.dependencies.dependencies.get_query_token)])


app.include_router(src.app.controllers.users.router)
app.include_router(src.app.controllers.items.router)
app.include_router(
    src.app.internal.admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(src.app.dependencies.dependencies.get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
