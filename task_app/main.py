import os
from fastapi import FastAPI

from task_app.auth.middlewares import ASGIAuthenticationMiddleware
from task_app.admin import routers as admin_routers

app = FastAPI()
app.add_middleware(ASGIAuthenticationMiddleware)


@app.get("/")
async def root():
    return {"message": "Welcome to test API"}


app.include_router(admin_routers.router)
