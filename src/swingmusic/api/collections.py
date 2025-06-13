"""
Contains all the collection routes.
"""

from typing import Any

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from swingmusic.db.userdata import CollectionTable
from swingmusic.lib.pagelib import recover_page_items, remove_page_items, validate_page_items
from swingmusic.utils.auth import get_current_userid

bp_tag = Tag(name="Collections", description="Collections")
api = APIBlueprint(
    "collections", __name__, url_prefix="/collections", abp_tags=[bp_tag]
)


class CreateCollectionBody(BaseModel):
    name: str = Field(description="The name of the collection")
    description: str = Field(description="The description of the collection")
    items: list[dict[str, Any]] = Field(
        description="The items to add to the collection",
        json_schema_extra={"example": [{"type": "album", "hash": "1234567890"}]},
    )


@api.post("")
def create_collection(body: CreateCollectionBody):
    """
    Create a new collection.
    """
    items = validate_page_items(body.items, existing=[])

    if len(items) == 0:
        return {"error": "No items to add"}, 400

    payload = {
        "name": body.name,
        "items": items,
        "userid": get_current_userid(),
        "extra": {
            "description": body.description,
        },
    }

    CollectionTable.insert_one(payload)

    return {"message": "collection created"}, 201


@api.get("")
def get_collections():
    """
    Get all collections.
    """
    return [collection for collection in CollectionTable.get_all()]


class AddCollectionItemBody(BaseModel):
    item: dict[str, Any] = Field(
        description="The item to add to the collection",
        json_schema_extra={"example": {"type": "album", "hash": "1234567890"}},
    )


class AddCollectionItemPath(BaseModel):
    collection_id: int = Field(
        description="The ID of the collection to add items to",
        json_schema_extra={"example": 1},
    )


@api.post("/<int:collection_id>/items")
def add_collection_item(path: AddCollectionItemPath, body: AddCollectionItemBody):
    """
    Add an item to a collection.
    """
    collection = CollectionTable.get_by_id(path.collection_id)

    if collection is None:
        return {"error": "Collection not found"}, 404

    new_items = validate_page_items([body.item], existing=collection["items"])

    if len(new_items) == 0:
        return {"error": "items already in collection"}, 400

    collection["items"].extend(new_items)
    CollectionTable.update_items(collection["id"], collection["items"])

    return {"message": "Items added to collection"}


class RemoveCollectionItemBody(BaseModel):
    item: dict[str, Any] = Field(
        description="The item to remove from the collection",
        json_schema_extra={"example": {"type": "album", "hash": "1234567890"}},
    )


class RemoveCollectionItemPath(BaseModel):
    collection_id: int = Field(
        description="The ID of the collection to remove items from"
    )


@api.delete("/<int:collection_id>/items")
def remove_collection_item(
    path: RemoveCollectionItemPath, body: RemoveCollectionItemBody
):
    """
    Remove an item from a collection.
    """
    collection = CollectionTable.get_by_id(path.collection_id)

    if collection is None:
        return {"error": "Collection not found"}, 404

    remaining = remove_page_items(collection["items"], body.item)
    CollectionTable.update_items(collection["id"], remaining)

    return {"message": "Item removed from collection"}


class GetCollectionBody(BaseModel):
    collection_id: int = Field(description="The ID of the collection to get")


@api.get("/<int:collection_id>")
def get_collection(path: GetCollectionBody):
    """
    Get a collection.
    """
    collection = CollectionTable.get_by_id(path.collection_id)
    if not collection:
        return {"error": "Collection not found"}, 404

    items = recover_page_items(collection["items"])
    return {
        "id": collection["id"],
        "name": collection["name"],
        "items": items,
        "extra": collection["extra"],
    }


class UpdateCollectionBody(BaseModel):
    name: str = Field(description="The name of the collection")
    description: str = Field(
        description="The description of the collection", default=""
    )


@api.put("/<int:collection_id>")
def update_collection(path: GetCollectionBody, body: UpdateCollectionBody):
    """
    Update a collection.
    """
    payload = {
        "id": path.collection_id,
        "name": body.name,
        "extra": {"description": body.description},
    }

    CollectionTable.update_one(payload)
    return payload


class DeleteCollectionPath(BaseModel):
    collection_id: int = Field(description="The ID of the collection to delete")


@api.delete("/<int:collection_id>")
def delete_collection(path: DeleteCollectionPath):
    """
    Delete a collection.
    """
    CollectionTable.delete_by_id(path.collection_id)
    return {"message": "Collection deleted"}
