from sqlalchemy import Column, Integer, String, Date
from app.db.base import Base

class Event(Base):
    __tablename__ = "eventos"

    id_evento = Column(Integer, primary_key=True, index=True)
    nombre_evento = Column(String(150), nullable=False)
    fecha_evento = Column(Date, nullable=False)
    lugar = Column(String(150), nullable=False)
    estado = Column(String(50), default="Activo")
