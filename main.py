from typing import Union
from fastapi import FastAPI
from actions import config_actions

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/clear_binding/{remote_id}")
def clear_binding(remote_id: str):
    print(remote_id)
    response = config_actions.runClearBinding(remote_id)
    return response