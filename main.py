from typing import Union
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from db import engine, get_db
from actions import (
    config_actions,
    radius_actions
)

SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.get("/user_by_id/{id}")
def get_by_id(
    id: int,
    db: Session = Depends(get_db())
):
    user = radius_actions.get_user(db,id)
    return user


@app.post("/clear_binding/{remote_id}")
def clear_binding(remote_id: str):
    print(remote_id)
    response = config_actions.runClearBinding(remote_id)
    return response