
# ! check fastapi version 
# from fastapi import FastAPI
# import fastapi

# print(fastapi.__version__)

# ! create basic server and get endpoint
# fastpapi dev main.py
from rich import print
from fastapi import FastAPI , Request
from mock_data import products
from dtos import Product_dto


app = FastAPI()
# http://127.0.0.1:8000
@app.get("/health")
def health():
    return "healthty"
@app.get("/")
def home():
    return "api is running"

@app.get("/contact")
def contact_us():
    return "you can connact us any time"
# http://127.0.0.1:8000/1
@app.get("/products")
def get_all_products():
    return products

# path parameter

@app.get("/products/{product_id}")
def get_one_product(product_id : int):
   
    for product in products:
        if product.get("id") == product_id:
            return product
    return {
        "erro" : "product not found"
    }
# query parameter

# @app.get("/greet")
# def greet(name : str , age : int):
#     return f"hello {name} how are you . your age is {age}"
@app.get("/greet")
def greet(request : Request):
    # print(request.query_params)
    query_params = dict(request.query_params)
    print(query_params)
    return f"hello {query_params.get('name')} how are you. your email is {query_params.get('age')}"


# differt tpyes of http method
# how to validate data - dtos
# how to call df http method


# sending data = body , header , request header , query params
# body > raw > json
@app.post("/create-product")
def create_product(data : Product_dto):
    # print(data)
    product_data = data.model_dump()
    # print(product_data)
    products.append(product_data)
    return {"status" : "product create successfully " , "data" : products }

@app.put("/update-product/{product_id}")
def update_product(product_data : Product_dto , product_id : int):
    for i, product in enumerate(products):
        # print(product , i)
        if product.get("id") == product_id:
            products[i]= product_data.model_dump()
            return {
        "status" : "product updated sucessfully", 
        "product" : product_data
    }
    return {
        "error" : "product not found with this id "
    }


@app.delete("/delete-product/{product_id}")
def delete_product(product_id: int):
    for i, product in enumerate(products):
        if product.get("id") == product_id:
            deleted_product = products.pop(i)
            return {
                "status": "product deleted successfully", 
                "product": deleted_product
            }
            
    return {
        "error": f"product not found with id {product_id}"
    }
