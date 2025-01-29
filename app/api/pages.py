"""
Contains all the page routes.
"""

from typing import Any

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from app.db.userdata import PageTable
from app.lib.pagelib import recover_page_items, remove_page_items, validate_page_items
from app.utils.auth import get_current_userid

bp_tag = Tag(name="Pages", description="Pages")
api = APIBlueprint("pages", __name__, url_prefix="/pages", abp_tags=[bp_tag])


class CreatePageBody(BaseModel):
    name: str = Field(description="The name of the page", example="My Page")
    description: str = Field(
        description="The description of the page", example="My Page"
    )
    items: list[dict[str, Any]] = Field(
        description="The items to add to the page",
        example=[{"type": "album", "hash": "1234567890"}],
    )


@api.post("")
def create_page(body: CreatePageBody):
    """
    Create a new page.
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

    PageTable.insert_one(payload)

    return {"message": "Page created"}, 201


@api.get("")
def get_pages():
    """
    Get all pages.
    """
    return PageTable.get_all()


class AddPageItemBody(BaseModel):
    item: dict[str, Any] = Field(
        description="The item to add to the page",
        example={"type": "album", "hash": "1234567890"},
    )


class AddPageItemPath(BaseModel):
    page_id: int = Field(description="The ID of the page to add items to", example=1)


@api.post("/<int:page_id>/items")
def add_page_item(path: AddPageItemPath, body: AddPageItemBody):
    """
    Add an item to a page.
    """
    page = PageTable.get_by_id(path.page_id)

    if page is None:
        return {"error": "Page not found"}, 404

    new_items = validate_page_items([body.item], existing=page["items"])

    if len(new_items) == 0:
        return {"error": "items already in page"}, 400

    page["items"].extend(new_items)
    PageTable.update_items(page["id"], page["items"])

    return {"message": "Items added to page"}


class RemovePageItemBody(BaseModel):
    item: dict[str, Any] = Field(
        description="The item to remove from the page",
        example={"type": "album", "hash": "1234567890"},
    )


class RemovePageItemPath(BaseModel):
    page_id: int = Field(description="The ID of the page to remove items from")


@api.delete("/<int:page_id>/items")
def remove_page_item(path: RemovePageItemPath, body: RemovePageItemBody):
    """
    Remove an item from a page.
    """
    page = PageTable.get_by_id(path.page_id)

    if page is None:
        return {"error": "Page not found"}, 404

    remaining = remove_page_items(page["items"], body.item)
    PageTable.update_items(page["id"], remaining)

    return {"message": "Item removed from page"}


class GetPageBody(BaseModel):
    page_id: int = Field(description="The ID of the page to get", example=1)


@api.get("/<int:page_id>")
def get_page(path: GetPageBody):
    """
    Get a page.
    """
    page = PageTable.get_by_id(path.page_id)
    if not page:
        return {"error": "Page not found"}, 404

    items = recover_page_items(page["items"])
    return {
        "id": page["id"],
        "name": page["name"],
        "items": items,
        "extra": page["extra"],
    }


class UpdatePageBody(BaseModel):
    name: str = Field(description="The name of the page")
    description: str = Field(description="The description of the page", default="")


@api.put("/<int:page_id>")
def update_page(path: GetPageBody, body: UpdatePageBody):
    """
    Update a page.
    """
    payload = {
        "id": path.page_id,
        "name": body.name,
        "extra": {"description": body.description},
    }

    PageTable.update_one(payload)
    return {"page": payload}


class DeletePagePath(BaseModel):
    page_id: int = Field(description="The ID of the page to delete")


@api.delete("/<int:page_id>")
def delete_page(path: DeletePagePath):
    """
    Delete a page.
    """
    PageTable.delete_by_id(path.page_id)
    return {"message": "Page deleted"}
