import os
from fastapi import FastAPI

from .admin import routers as admin_routers

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to test API"}


app.include_router(admin_routers.router)
