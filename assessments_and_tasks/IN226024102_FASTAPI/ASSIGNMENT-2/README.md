# FastAPI Day-2 Assignment

This repository contains the FastAPI Day-2 practice assignment completed as part of the internship training.

## Features Implemented

1. **Product Filtering API**
   - Filter products by category, minimum price, and maximum price.

2. **Product Price Endpoint**
   - Get only the name and price of a product using its ID.

3. **Customer Feedback API**
   - Submit feedback with validation using Pydantic.
   - Rating must be between 1 and 5.
   - Comment is optional.

4. **Product Summary Dashboard**
   - Shows total products, stock status, cheapest and most expensive products, and categories.

5. **Bulk Order API**
   - Place orders with multiple items.
   - Handles out-of-stock and invalid products.

6. **Bonus – Order Status Tracker**
   - Orders start with **pending** status.
   - Can be confirmed using PATCH endpoint.

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn

## How to Run the Project

Install dependencies:

pip install fastapi  
pip install uvicorn

Run the server:

uvicorn main:app --reload

Open Swagger documentation:

http://127.0.0.1:8000/docs

## Project Structure

