from pymongo import MongoClient
from pydantic import BaseModel
from typing import Union
from schematics.types import StringType
from schematics.models import Model


def get_db():
    mongo_uri = 'mongodb+srv://hemraj348:hemraj123@cluster0.exqmcbu.mongodb.net'
    client = MongoClient(mongo_uri)
    db = client['customer_data']
    return db


class CustomerData(BaseModel):
    cust_name: str
    cust_email: str
    cust_phone: str
    cust_password: str


class ResponseDto(BaseModel):
    cust_name: str
    cust_email: str
    cust_phone: str
    cust_password: str

    class Config:
        exclude = {'cust_id'}


class SellerData(BaseModel):
    seller_name: str
    seller_phone: Union[str, None] = None
    seller_password: str
    seller_email: str
    seller_address: Union[str, None] = None


def create_customer(customer: CustomerData):
    users_collection = get_db().users
    users_collection.insert_one(customer.dict(by_alias=True))
    return customer.dict()
