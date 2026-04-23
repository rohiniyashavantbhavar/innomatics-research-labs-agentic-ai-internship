from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional
import math

# Application configuration
app = FastAPI(
    title="Food Delivery API",
    description="Backend system for managing menu, orders, cart, and delivery workflow",
    version="1.0.0"
)

# In-memory data storage
menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 250, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veg Burger", "price": 120, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Chocolate Cake", "price": 180, "category": "Dessert", "is_available": False},
    {"id": 5, "name": "Paneer Pizza", "price": 300, "category": "Pizza", "is_available": True},
    {"id": 6, "name": "French Fries", "price": 90, "category": "Snack", "is_available": True},
]

orders = []
order_counter = 1
cart = []

# Utility functions
def find_menu_item(item_id: int):
    """Return a menu item by ID or None if not found."""
    return next((item for item in menu if item["id"] == item_id), None)

def calculate_bill(price: int, quantity: int, order_type: str):
    """Calculate total price including delivery charge."""
    total = price * quantity
    if order_type == "delivery":
        total += 30
    return total

def filter_menu_logic(category, max_price, is_available):
    """Apply filtering on menu items."""
    result = menu
    if category is not None:
        result = [i for i in result if i["category"].lower() == category.lower()]
    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]
    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]
    return result

# Request models
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"

class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

# Home endpoint
@app.get("/", summary="Health check endpoint")
def home():
    """Verify API is running."""
    return {"message": "Welcome to Food Delivery API"}

# Menu endpoints
@app.get("/menu", summary="Get all menu items")
def get_menu():
    """Return all available menu items."""
    return {"total": len(menu), "items": menu}

@app.get("/menu/summary", summary="Get menu summary")
def menu_summary():
    """Return summary of menu including availability and categories."""
    available = [i for i in menu if i["is_available"]]
    return {
        "total": len(menu),
        "available": len(available),
        "unavailable": len(menu) - len(available),
        "categories": list(set(i["category"] for i in menu))
    }

@app.get("/menu/search", summary="Search menu items")
def search_menu(keyword: str):
    """Search menu items by name or category."""
    result = [
        i for i in menu
        if keyword.lower() in i["name"].lower()
        or keyword.lower() in i["category"].lower()
    ]
    if not result:
        return {"message": "No items found"}
    return {"total_found": len(result), "items": result}

@app.get("/menu/filter", summary="Filter menu items")
def filter_menu(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    is_available: Optional[bool] = None
):
    """Filter menu based on category, price, and availability."""
    result = filter_menu_logic(category, max_price, is_available)
    return {"count": len(result), "items": result}

@app.get("/menu/sort", summary="Sort menu items")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    """Sort menu items by given field and order."""
    if sort_by not in ["price", "name", "category"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    result = sorted(menu, key=lambda x: x[sort_by], reverse=(order == "desc"))
    return {"sorted_by": sort_by, "order": order, "items": result}

@app.get("/menu/page", summary="Paginate menu items")
def paginate(page: int = 1, limit: int = 3):
    """Return paginated menu items."""
    start = (page - 1) * limit
    total_pages = math.ceil(len(menu) / limit)

    return {
        "page": page,
        "limit": limit,
        "total": len(menu),
        "total_pages": total_pages,
        "items": menu[start:start + limit]
    }

@app.get("/menu/browse", summary="Combined search, sort, and pagination")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    """Apply search, sorting, and pagination in a single endpoint."""
    result = menu

    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    result = sorted(result, key=lambda x: x[sort_by], reverse=(order == "desc"))

    start = (page - 1) * limit
    total_pages = math.ceil(len(result) / limit)

    return {
        "total": len(result),
        "page": page,
        "total_pages": total_pages,
        "items": result[start:start + limit]
    }

@app.get("/menu/{item_id}", summary="Get menu item by ID")
def get_item(item_id: int):
    """Retrieve a menu item using its ID."""
    item = find_menu_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Order endpoints
@app.get("/orders", summary="Get all orders")
def get_orders():
    """Return all orders."""
    return {"total_orders": len(orders), "orders": orders}

@app.post("/orders", summary="Create a new order")
def create_order(order: OrderRequest):
    """Create an order for a menu item."""
    global order_counter

    item = find_menu_item(order.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if not item["is_available"]:
        raise HTTPException(status_code=400, detail="Item not available")

    total = calculate_bill(item["price"], order.quantity, order.order_type)


    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total_price": total
    }

    orders.append(new_order)
    order_counter += 1

    return new_order

# CRUD operations
@app.post("/menu", summary="Add a new menu item")
def add_menu(item: NewMenuItem, response: Response):
    """Add a new item to the menu."""
    if any(m["name"].lower() == item.name.lower() for m in menu):
        raise HTTPException(status_code=400, detail="Item already exists")

    new_item = item.dict()
    new_item["id"] = len(menu) + 1
    menu.append(new_item)

    response.status_code = 201
    return new_item

@app.put("/menu/{item_id}", summary="Update menu item")
def update_menu(item_id: int, price: Optional[int] = None, is_available: Optional[bool] = None):
    """Update price or availability of a menu item."""
    item = find_menu_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if price is not None:
        item["price"] = price
    if is_available is not None:
        item["is_available"] = is_available

    return item

@app.delete("/menu/{item_id}", summary="Delete menu item")
def delete_menu(item_id: int):
    """Remove a menu item."""
    item = find_menu_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    menu.remove(item)
    return {"message": "Item deleted successfully"}

# Cart workflow
@app.post("/cart/add", summary="Add item to cart")
def add_to_cart(item_id: int, quantity: int = 1):
    """Add or update item in cart."""
    item = find_menu_item(item_id)
    if not item or not item["is_available"]:
        raise HTTPException(status_code=400, detail="Item unavailable")

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Quantity updated", "cart": cart}

    cart.append({"item_id": item_id, "quantity": quantity})
    return {"message": "Item added to cart", "cart": cart}

@app.get("/cart", summary="View cart")
def view_cart():
    """Return all items in cart with total cost."""
    total = 0
    details = []

    for c in cart:
        item = find_menu_item(c["item_id"])
        cost = item["price"] * c["quantity"]
        total += cost
        details.append({"item": item["name"], "quantity": c["quantity"], "cost": cost})

    return {"cart": details, "grand_total": total}

@app.delete("/cart/{item_id}", summary="Remove item from cart")
def remove_cart(item_id: int):
    """Remove an item from the cart."""
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Item removed"}
    raise HTTPException(status_code=404, detail="Item not in cart")

@app.post("/cart/checkout", summary="Checkout cart")
def checkout(data: CheckoutRequest, response: Response):
    """Convert cart items into orders."""
    global order_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    new_orders = []

    for c in cart:
        item = find_menu_item(c["item_id"])
        price = item["price"] * c["quantity"]

        order = {
            "order_id": order_counter,
            "customer": data.customer_name,
            "item": item["name"],
            "total_price": price
        }

        total += price
        orders.append(order)
        new_orders.append(order)
        order_counter += 1

    cart.clear()
    response.status_code = 201

    return {"orders": new_orders, "grand_total": total}

# Search Orders
@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [
        order for order in orders
        if customer_name.lower() in order["customer_name"].lower()
    ]

    if not result:
        return {"message": "No orders found"}

    return {"total_found": len(result), "orders": result}

# Sort Orders
@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    sorted_orders = sorted(
        orders,
        key=lambda x: x["total_price"],
        reverse=(order == "desc")
    )

    return {"order": order, "orders": sorted_orders}