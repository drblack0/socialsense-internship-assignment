from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"))
    status = Column(String, default="draft")
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    author = relationship("User", back_populates="posts")
    reactions = relationship("PostReaction", back_populates="post")
    analytics = relationship("PostAnalytics", uselist=False, back_populates="post")


class PostReaction(Base):
    __tablename__ = "post_reactions"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    reaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    post = relationship("Post", back_populates="reactions")
    user = relationship("User")
    __table_args__ = (UniqueConstraint("post_id", "user_id", name="_post_user_uc"),)


class PostAnalytics(Base):
    __tablename__ = "post_analytics"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("post.id"), unique=True)
    total_reactions = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    total_impressions = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    praise_count = Column(Integer, default=0)
    empathy_count = Column(Integer, default=0)
    interest_count = Column(Integer, default=0)
    appreciation_count = Column(Integer, default=0)

    post = relationship("Post", back_populates="analytics")
