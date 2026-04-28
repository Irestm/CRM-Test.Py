from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Boolean
from src.core.database import Base

class ClientModel(Base):
    __tablename__ = "clients"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str] = mapped_column(String(50))

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    tasks: Mapped[List["TaskModel"]] = relationship(back_populates="user")

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="new")
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped["UserModel"] = relationship(back_populates="tasks")