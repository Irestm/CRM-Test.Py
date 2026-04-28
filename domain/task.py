from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    user_id = Column(Integer)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    description = Column(String, nullable=True)
    status = Column(String, default="new")
    task_type = Column(String, default="sale")
    company_name = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    comment = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)

    client = relationship("Client", back_populates="tasks")
    files = relationship("TaskFile", back_populates="task", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="task", cascade="all, delete-orphan")
