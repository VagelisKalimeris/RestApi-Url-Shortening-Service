from redis import Redis
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.shortener_service import shorten_url_logic, retrieve_url_logic
from app.routers.router_dependencies import get_redis, get_postgres
from app.models.shortener_route_models import ShortenOpDetails, ShortenOpResult, RetrieveOpResult, RetrieveOpDetails
from app.models.shared_models import PrettyJSONResponse, Error


router = APIRouter()


@router.post('/shorten-url', status_code=201, response_class=PrettyJSONResponse)
def shorten_url(op_details: ShortenOpDetails, cache: Redis = Depends(get_redis),
                db: Session = Depends(get_postgres)) -> dict:
    """
    Shortens given link. Adds db entry. Returns shortened link.
    """
    # Check for errors
    if isinstance(url_shorten_res := shorten_url_logic(op_details.user_id, op_details.original_url,
                                                       op_details.postfix, op_details.expiration, cache, db), Error):
        raise HTTPException(status_code=url_shorten_res.status, detail=url_shorten_res.message)

    shorten_url_result = ShortenOpResult('Redirection URL created successfully!', op_details.user_id,
                                         url_shorten_res.short_url, op_details.expiration)

    return shorten_url_result.__dict__


@router.get('/retrieve-url', status_code=200, response_class=PrettyJSONResponse)
def retrieve_url(user_id: int, short_url: str, cache: Redis = Depends(get_redis),
                 db: Session = Depends(get_postgres)) -> dict:
    """
    Retrieves original URL entry, from given short URL.
    """
    if isinstance(postfix := RetrieveOpDetails.validate_short_url_and_retrieve_postfix(short_url), Error):
        raise HTTPException(status_code=postfix.status, detail=postfix.message)

    # Check for errors
    if isinstance(url_retrieval_res := retrieve_url_logic(user_id, postfix, cache, db), Error):
        raise HTTPException(status_code=url_retrieval_res.status, detail=url_retrieval_res.message)

    shorten_op_result = RetrieveOpResult('Original URL retrieved successfully!', user_id,
                                         url_retrieval_res.original_url, url_retrieval_res.expiration,
                                         url_retrieval_res.cached_result)

    return shorten_op_result.__dict__
