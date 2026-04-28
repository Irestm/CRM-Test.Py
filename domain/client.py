from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from domain.task import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    position = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="client")
