from pydantic import BaseModel

class Product_dto(BaseModel):
    id: int
    title: str
    price: float = 0
    count: int = 0
