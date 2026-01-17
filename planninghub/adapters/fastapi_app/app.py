"""FastAPI application wiring."""

from fastapi import FastAPI

from planninghub.adapters.fastapi_app.routes import router

app = FastAPI()
app.include_router(router)
