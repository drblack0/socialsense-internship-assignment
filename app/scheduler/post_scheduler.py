import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app import crud, models
from app.db.session import SessionLocal


async def schedule_checker():
    while True:
        db: Session = SessionLocal()
        now = datetime.utcnow()
        scheduled_posts = (
            db.query(models.Post)
            .filter(models.Post.status == "scheduled", models.Post.scheduled_at <= now)
            .all()
        )

        for post in scheduled_posts:
            # Simulate the LinkedIn API post request
            print(f"Publishing post: {post.id}")
            post.status = "published"
            post.published_at = now
            db.add(post)
            db.commit()

        db.close()
        await asyncio.sleep(60)  # Check every minute
