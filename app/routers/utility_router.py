import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from app.models.shared.shared_models import PrettyJSONResponse
from app.models.route.utility_route_models import StatusResult, ServerStatsResult
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
def api_status() -> StatusResult:
    """
    Utility route for testing api functionality.
    """
    return StatusResult(
        message='URL Shortening Service is up and running!'
    )


@router.get('/server_statistics', status_code=200, response_class=PrettyJSONResponse)
def server_stats() -> ServerStatsResult:
    """
    Utility route, returns API usage information.
    """
    server_statistics = retrieve_server_statistics()

    return ServerStatsResult(
        message='Server statistics retrieved successfully!',
        statistics=server_statistics.__dict__
    )
