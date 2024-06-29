from datetime import date
from urllib.parse import urlsplit

from pydantic import BaseModel, Field, model_validator

from app.config import POSTFIX_LENGTH, SERVICE_BASE_URL
from app.models.shared.shared_models import Error


class ShortenOpDetails(BaseModel):
    """
    Purposed for POST request body validation.
    """
    user_id: int = Field(json_schema_extra={'example': 555})
    original_url: str = Field(json_schema_extra={'example': 'https://www.example.com/original-url'})
    postfix: str | None = Field(json_schema_extra={'example': '47xes'}, default=None)
    expiration: date = Field(json_schema_extra={'example': '2024-12-31'}, default=None)

    @model_validator(mode='after')
    def postfix_is_valid(self):
        if self.postfix and (postfix_length := len(self.postfix)) != POSTFIX_LENGTH:
            raise ValueError(f'Postfix length should be \'{POSTFIX_LENGTH}\', instead it was \'{postfix_length}\'!')
        return self

    @model_validator(mode='after')
    def expiration_is_valid(self):
        if self.expiration < date.today():
            raise ValueError('Short URL cannot expire on past date!')
        return self


class RetrieveOpDetails:
    """
    Purposed for GET request param validation.
    """
    @staticmethod
    def validate_short_url_and_retrieve_postfix(short_url: str) -> str | Error:
        split_url = urlsplit(short_url)
        base_url, postfix = split_url.netloc, split_url.path.strip('/')
        if base_url != urlsplit(SERVICE_BASE_URL).netloc:
            return Error('Given URL does not belong to this service!', 422)
        if len(postfix) != POSTFIX_LENGTH:
            return Error(f'Given URL has incorrect postfix length. {POSTFIX_LENGTH} was expected, but '
                         f'{len(postfix)} was given!', 422)
        return postfix


class ShortenOpResult(BaseModel):
    """
    Shortening service POST response template.
    """
    message: str = Field(json_schema_extra={'example': 'Redirection URL created successfully!'})
    user_id: int = Field(json_schema_extra={'example': 555})
    shortened_url: str = Field(json_schema_extra={'example': 'https://shrinkurl.com/47xes'})
    expiration: date = Field(json_schema_extra={'example': '2024-12-31'})


class RetrieveOpResult(BaseModel):
    """
    Shortening service GET response template.
    """
    message: str = Field(json_schema_extra={'example': 'Original URL retrieved successfully!'})
    user_id: int = Field(json_schema_extra={'example': 555})
    original_url: str = Field(json_schema_extra={'example': 'https://www.example.com/original-url'})
    expiration: date = Field(json_schema_extra={'example': '2024-12-31'})
    cached_result: bool = Field(json_schema_extra={'example': False})
