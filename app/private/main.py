from fastapi import FastAPI
from routers import example as example_router

app = FastAPI()

app.include_router(example_router.router)