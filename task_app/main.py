import os
from fastapi import FastAPI

from .auth import routers as auth_routers

app = FastAPI()


@app.get("/")
async def root():
    return {"message": os.environ["MONGODB_URL"]}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(auth_routers.router)
