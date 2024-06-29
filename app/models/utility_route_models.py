from pydantic import BaseModel, Field


class StatusResult(BaseModel):
    """
    Api status response template.
    """
    message: str = Field(json_schema_extra={'example': 'URL Shortening Service is up and running!'})


class ServerStatsResult(BaseModel):
    """
    Server statistics response template.
    """
    message: str = Field(json_schema_extra={'example': 'Server statistics retrieved successfully!'})
    statistics: dict = Field(
        description='Current run server use statistics.',
        json_schema_extra={
            'example': {
                'cache_reads': 0,
                'db_reads': 0,
                'db_writes': 0,
                'read_errors': 0,
                'write_errors': 0
            }
        }
    )
