"""
Reusable Pydantic basic schemas for the API
"""

from pydantic import BaseModel, Field

from swingmusic.settings import Defaults


class AlbumHashSchema(BaseModel):
    """
    Extending this class will give you a model with the `albumhash` field
    """

    albumhash: str = Field(
        description="The album hash",
        json_schema_extra={
            "example": Defaults.API_ALBUMHASH,
        },
        min_length=Defaults.HASH_LENGTH,
        max_length=Defaults.HASH_LENGTH,
    )


class ArtistHashSchema(BaseModel):
    """
    Extending this class will give you a model with the `artisthash` field
    """
    artisthash: str = Field(
        description="The artist hash",
        json_schema_extra={
            "example": Defaults.API_ARTISTHASH,
        },
        min_length=Defaults.HASH_LENGTH,
        max_length=Defaults.HASH_LENGTH,
    )


class TrackHashSchema(BaseModel):
    """
    Extending this class will give you a model with the `trackhash` field
    """

    trackhash: str = Field(
        description="The track hash",
        json_schema_extra={
            "example": Defaults.API_TRACKHASH,
        },
        min_length=Defaults.HASH_LENGTH,
        max_length=Defaults.HASH_LENGTH,
    )


class GenericLimitSchema(BaseModel):
    """
    Extending this class will give you a model with the `limit` field
    """

    limit: int = Field(
        description="The number of items to return",
        json_schema_extra={
            "example": Defaults.API_CARD_LIMIT,
        },
        default=Defaults.API_CARD_LIMIT,
    )


# INFO: The following 3 classes are duplicated to specify the type of items
class TrackLimitSchema(BaseModel):
    """
    Extending this class will give you a model with the `limit` field
    """

    limit: int = Field(
        description="The number of tracks to return",
        json_schema_extra={
            "example": Defaults.API_CARD_LIMIT,
        },
        default=5,
        alias="tracklimit",
    )


class AlbumLimitSchema(BaseModel):
    """
    Extending this class will give you a model with the `limit` field
    """

    limit: int = Field(
        description="The number of albums to return",
        json_schema_extra={
            "example": Defaults.API_CARD_LIMIT,
        },
        default=Defaults.API_CARD_LIMIT,
        alias="albumlimit",
    )


class ArtistLimitSchema(BaseModel):
    """
    Extending this class will give you a model with the `limit` field
    """

    limit: int = Field(
        description="The number of artists to return",
        json_schema_extra={
            "example": Defaults.API_CARD_LIMIT,
        },
        default=Defaults.API_CARD_LIMIT,
        alias="artistlimit",
    )
