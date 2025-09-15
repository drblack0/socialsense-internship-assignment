from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Post)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.PostCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    post = crud.post.create_with_owner(db=db, obj_in=post_in, author_id=current_user.id)
    return post


@router.get("/", response_model=List[schemas.Post])
def read_posts(
    db: Session = Depends(deps.get_db),
    user_id: Optional[int] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    current_user: models.User = Depends(deps.get_current_user),
):
    if current_user.role != "admin":
        user_id = current_user.id
    posts = crud.post.get_filtered(
        db, user_id=user_id, start_time=start_time, end_time=end_time
    )
    return posts


@router.get("/analytics/top-engaging", response_model=List[schemas.Post])
def get_top_engaging_posts(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
):
    posts = crud.post.get_top_engaging_posts(db)
    return posts
