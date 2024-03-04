from fastapi import FastAPI, Query, HTTPException
from starlette.responses import JSONResponse
from dbconnection import ResponseDto, get_db, SellerData, CustomerData
import logging

app = FastAPI()
db = get_db()


# post data
@app.post("/signUp", response_model=CustomerData)
async def signup(data: CustomerData):
    try:
        if db.users.find_one({"email": data.cust_email}):
            raise HTTPException(status_code=400, detail="email already exists")

        db.users.insert_one(data.dict())
        return data
    except Exception as e:
        logging.error(e)


# get particular data
@app.get("/getData")
async def get_particular_data(email: str = Query(None)):
    try:
        logging.info(f"Fetching data for email: {email}")
        user = db.users.find_one({"cust_email": email})
        logging.info(user)
        if user:
            dto = ResponseDto(
                cust_email=user['cust_email'],
                cust_name=user['cust_name'],
                cust_phone=user['cust_phone'],
                cust_password=user['cust_password']
            )
            return dto.dict()
        else:
            return {"message": "Customer not found"}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"message": e}


# get data
@app.get("/getAllData")
async def get_all_data():
    try:
        get_data = db.users
        all_users = list(get_data.find())
        response_data = [ResponseDto(**data).dict() for data in all_users]
        return JSONResponse(status_code=200, content=response_data)
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))


# delete data
@app.delete("/deleteRecord")
async def delete_data(email: str = Query(None)):
    try:
        data_count = db.users.count_documents({"cust_email": email})
        if data_count > 0:
            db.users.delete_one({"cust_email": email})
            logging.info(f"Deleted {email} from database")
            return {"detail : ", "The data is been deleted from Database"}
        else:
            logging.info(f'No data found for {email}')
            return {"detail": "No data found for the email specified"}
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"detail": str(e)}


# post request body
@app.post("/getRequestBodyData")
async def get_request_data(seller: SellerData):
    try:
        if len(seller.seller_phone) >= 10:
            dto = SellerData(
                seller_phone=seller.seller_phone,
                seller_name=seller.seller_name,
                seller_address=seller.seller_address,
                seller_email=seller.seller_email,
                seller_password=seller.seller_password
            )
            return dto
        else:
            logging.error(f"data not correctly formatted")
    except Exception as e:
        logging.error({e})


@app.put("/updateData")
async def update_request_data(customer: CustomerData, email: str = Query(...)):
    try:
        existing_user = db.users.find_one({"cust_email": email})
        if not existing_user:
            raise HTTPException(status_code=404, detail="email not found")

        updated_user = db.users.update_many(
            {"cust_email": email},
            {"$set": customer.dict(exclude_unset=True)}
        )
        if updated_user.modified_count == 0:
            raise HTTPException(status_code=304, detail="no changes applied")
        return customer
    except Exception as e:
        logging.error(f"An error occurred: {e}")
