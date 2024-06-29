################################################################################
#         For API trial and documentation visit http://localhost/docs          #
################################################################################
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_middleware_logger.fastapi_middleware_logger import add_custom_logger

from app.repositories.db_repository.postgres import engine
from app.models.data.sqlalchemy_models import Base
from app.routers import utility_router, shortener_router
from app.routers.utility_router import lifespan


def customize_openapi_schema():
    """
    Updates OpenAPI documentation details for SWAGGER UI.
    """
    openapi_schema = get_openapi(
        title='Simple URL shortener',
        version='1.0.0',
        summary='API for URL shortening service.',
        # description=open('README.md', 'r').read(350),
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Start database
Base.metadata.create_all(bind=engine)

# Start API
app = FastAPI(lifespan=lifespan)

# Enable routes
app.include_router(shortener_router.router)
app.include_router(utility_router.router)


# Manage detailed logging
log_abs_path = str(Path(__file__).resolve().parent.parent) + '/logs/api_full.log'

logging.basicConfig(level=logging.INFO, filename=log_abs_path,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = add_custom_logger(app, disable_uvicorn_logging=False)

# Customize SWAGGER
app.openapi = customize_openapi_schema
