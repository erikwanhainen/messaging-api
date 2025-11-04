from fastapi import FastAPI
from app.api import messages, health
from app.logger import configure_logging

configure_logging()


app = FastAPI(
    title="Message Service API",
    description="""A REST API for sending and retrieving messages.""",
    version="1.0.0",
    contact={"name": "Erik Wanhainen"},
)

app.include_router(health.router)
app.include_router(messages.router)
