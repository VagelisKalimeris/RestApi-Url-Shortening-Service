import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from app.models.shared_models import PrettyJSONResponse
from app.models.utility_route_models import StatusResult, ServerStatsResult
from app.services.shortener_service import retrieve_server_statistics

router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """
    Sets up compact logging, for all API requests.
    """
    logger = logging.getLogger('uvicorn.access')
    handler = logging.handlers.RotatingFileHandler('logs/api_short.log', mode='a', maxBytes=100*1024, backupCount=3)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    yield


@router.get('/status', status_code=200, response_class=PrettyJSONResponse)
def api_status() -> dict:
    """
    Utility route for testing api functionality.
    """
    return StatusResult('URL Shortening Service is up and running!').__dict__


@router.get('/server_statistics', status_code=200, response_class=PrettyJSONResponse)
def server_stats() -> dict:
    """
    Utility route, returns API usage information.
    """
    server_statistics = retrieve_server_statistics()

    return ServerStatsResult('Server statistics retrieved successfully!', server_statistics.__dict__).__dict__
