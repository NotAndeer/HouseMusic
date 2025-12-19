from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.event import Event

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "API House Music funcionando correctamente"}
