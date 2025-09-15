from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.posts import Post, PostAnalytics
from app.schemas.post import PostCreate
from datetime import datetime


class CRUDPost(CRUDBase[Post, PostCreate, PostCreate]):
    def create_with_owner(
        self, db: Session, *, obj_in: PostCreate, author_id: int
    ) -> Post:
        db_obj = Post(**obj_in.dict(), author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_filtered(
        self,
        db: Session,
        *,
        user_id: Optional[int],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
    ) -> List[Post]:
        query = db.query(self.model)
        if user_id:
            query = query.filter(Post.author_id == user_id)
        if start_time:
            query = query.filter(Post.published_at >= start_time)
        if end_time:
            query = query.filter(Post.published_at <= end_time)
        return query.all()

    def get_top_engaging_posts(self, db: Session, limit: int = 5) -> List[Post]:
        return (
            db.query(Post)
            .join(PostAnalytics)
            .order_by(PostAnalytics.total_reactions.desc())
            .limit(limit)
            .all()
        )


post = CRUDPost(Post)
