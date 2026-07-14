from fastapi import FastAPI
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


@app.get("/")
def Welcome():
    return "Welcome to my fastapi api. This api is build to pass local drive information to user ui"


@app.post("/auth/{password}")
def auth(password):
    
    return os.environ.get("WEBPASS") == password if os.environ.get("JWTS") else None
