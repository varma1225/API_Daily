from fastapi import FastAPI,HTTPException
from datetime import datetime
from pydantic import BaseModel
import random
import uuid

from webhooks.phone_number_validation import Phone

class Data(BaseModel):
      customer_name:str
      phone: str
      service: str
      booking_date: str
      booking_time: str

customers_data=[]

app=FastAPI()
@app.post("/bookings")
async def create_booking(data:Data):

    try:
      data = data.model_dump()
      services=["plumbing","electrical","ac repair"]
      phone_number=(data.get("phone"))
      customer_name=data.get("customer_name")
      
      booking_date_str=data.get("booking_date")+" "+data.get("booking_time")
      booking_date=datetime.strptime(booking_date_str,"%Y-%m-%d %H:%M")

      
      service=data.get("service").lower()
      current_date=datetime.now()
      if len(phone_number)!=10 or not phone_number.isdigit():
            raise HTTPException(status_code=422,detail="phone number is invalid")
      if service not in services :
            raise HTTPException(status_code=422,detail="invalid service")
      if  booking_date < current_date:
            raise HTTPException(status_code=400,detail="invalid date to book an appointment")
      booking_id=str(uuid.uuid4())
      data["booking_id"]=booking_id
      customers_data.append(data)
      return {"message":f"Hi {customer_name},your appointment has been booked succesfully  on {booking_date} ,here is your id {booking_id} by using this you can check our appointment status ,Thank you!","cust_data":data}
            
    except HTTPException as e:
         raise e
    except Exception as e:
         print(e)
         raise HTTPException(status_code=500,detail="internal error")

