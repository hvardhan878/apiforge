from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Mock data store
mock_items = [
    {"id": 1, "name": "Item One", "description": "First item description"},
    {"id": 2, "name": "Item Two", "description": "Second item description"},
]

# Pydantic model for Item
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

@router.get("/", response_model=List[Item])
def list_items():
    return mock_items

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in mock_items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    new_id = max(i["id"] for i in mock_items) + 1 if mock_items else 1
    new_item = {"id": new_id, **item.dict()}
    mock_items.append(new_item)
    return new_item

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    for idx, existing_item in enumerate(mock_items):
        if existing_item["id"] == item_id:
            updated_item = {"id": item_id, **item.dict()}
            mock_items[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    for idx, existing_item in enumerate(mock_items):
        if existing_item["id"] == item_id:
            del mock_items[idx]
            return
    raise HTTPException(status_code=404, detail="Item not found")