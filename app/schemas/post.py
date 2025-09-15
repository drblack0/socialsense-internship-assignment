from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    author_id: int
    status: str
    published_at: Optional[datetime]

    class Config:
        orm_mode = True


class PostAnalyticsData(BaseModel):
    total_reactions: int
    total_engagement: int
    total_impressions: int
    total_shares: int
    total_comments: int

    class Config:
        orm_mode = True
