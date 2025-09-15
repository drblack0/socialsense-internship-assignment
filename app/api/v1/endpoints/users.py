from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps  
from app.models.user import User
from app.schemas.user import User as SchemaUser, UserCreate

from app.crud.crud_user import user as user_crud

router = APIRouter()


@router.post("/", response_model=SchemaUser)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.get_current_active_admin),
):
    existing_user = user_crud.get_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = user_crud.create(db, obj_in=user_in)
    return new_user


@router.get("/", response_model=List[SchemaUser])
def read_users(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
):
    users = user_crud.get_multi(db)
    return users
