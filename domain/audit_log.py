from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from domain.task import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer)
    action = Column(String)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    task = relationship("Task", back_populates="audit_logs")
