import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..dao import user as crud
from ..dependencies.dependencies import get_db
from ..dto import user as schemas

router = APIRouter()


@router.post("/users/",
             response_model=schemas.User,
             tags=["User"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logging.info("This is message..!!")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/",
            response_model=List[schemas.User],
            tags=["User"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}",
            response_model=schemas.User,
            tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
