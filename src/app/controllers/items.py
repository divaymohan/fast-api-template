import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..dao import item as crud
from ..dependencies.dependencies import get_db
from ..dto import item as schemas

router = APIRouter()

logger = logging.getLogger()


@router.post("/users/{user_id}/items/",
             response_model=schemas.Item,
             tags=["items"])
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    logger.warning("This is message..!!")
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/",
            response_model=List[schemas.Item],
            tags=["items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
