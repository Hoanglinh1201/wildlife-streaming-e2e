import logging

from fastapi import FastAPI

from backend.server.lifespan import lifespan
from backend.server.routes import router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)
app.include_router(router)
