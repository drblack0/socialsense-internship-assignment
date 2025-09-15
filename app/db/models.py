from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    posts = relationship("Post", back_populates="user", cascade="all, delete")

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'user')", name="check_user_role"),
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="draft")
    scheduled_time = Column(TIMESTAMP, nullable=True)
    published_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="posts")
    analytics = relationship(
        "PostAnalytics", back_populates="post", cascade="all, delete"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'scheduled', 'published')", name="check_post_status"
        ),
    )


class PostAnalytics(Base):
    __tablename__ = "post_analytics"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    likes = Column(Integer, default=0)
    praise = Column(Integer, default=0)
    empathy = Column(Integer, default=0)
    interest = Column(Integer, default=0)
    appreciation = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    post = relationship("Post", back_populates="analytics")
