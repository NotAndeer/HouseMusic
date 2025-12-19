from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
