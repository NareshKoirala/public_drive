from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
def Welcome():
    return "Welcome to my fastapi api. This api is build to pass local drive information to user ui"


@app.post("/auth/{password}")
def auth(password):
    return
