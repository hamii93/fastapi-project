from fastapi import FastAPI, HTTPException
from models import Item
from typing import Optional

app = FastAPI()


inventory_db = [
    {"id": 1, "name": "laptop", "quantity": 100, "price": 999.99},
    {"id": 2, "name": "Monitor", "quantity": 200, "price": 199.99},
    {"id": 3, "name": "Keyboard", "quantity": 300, "price": 49.99},
    {"id": 4, "name": "Mouse", "quantity": 400, "price": 29.99},
    {"id": 5, "name": "Printer", "quantity": 500, "price": 149.99},
]
@app.get("/")
async def root():
    return {"message": "Welcome to NextGen Logistics"}

@app.get("/items")
async def get_inventory(limit : int = 10, search: Optional[str] = None):
    if search:
        filtered_items = [item for item in inventory_db if search.lower() in item["name"].lower()]
        return {"items": filtered_items[:limit]}
    return {"items": inventory_db[:limit]}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    for item in inventory_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items")
async def add_item(item: Item):
    for existing_item in inventory_db:
        if existing_item["id"] == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists")
    inventory_db.append(item.model_dump())
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(inventory_db):
        if item["id"] == item_id:
            updated_item.id = item_id 
            inventory_db[index] = updated_item.model_dump()
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for index, item in enumerate(inventory_db):
        if item["id"] == item_id:
            inventory_db.pop(index)
            return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")