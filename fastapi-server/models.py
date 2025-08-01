from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
import uuid
from database import Base  # use absolute import if needed

def generate_uuid():
    return str(uuid.uuid4())

class Note(Base):
    __tablename__ = "notes"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    tags_json = Column(Text, default="[]", nullable=False)  # :white_check_mark: Add this line
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
