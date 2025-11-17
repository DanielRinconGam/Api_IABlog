from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)
    description = Column(String(255), nullable=True)

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    post = relationship("Post", back_populates="images")
