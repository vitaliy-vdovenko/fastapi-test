import os
from fastapi import FastAPI

from .admin import routers as admin_routers
from .auth import routers as auth_routers

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to test API"}


app.include_router(admin_routers.router)
app.include_router(auth_routers.router)
