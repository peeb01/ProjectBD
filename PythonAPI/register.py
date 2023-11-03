from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from datetime import date, datetime
from pydantic import BaseModel, Field

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-M9VL3MH\SQLEXPRESS'
DATABASE_NAME = 'PP'



connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"

conn = pyodbc.connect(connection_string)

cursor = conn.cursor()




app = FastAPI()

class CustomerRegistration(BaseModel):
    username: str
    pasword: str
    fname: str
    lname: str
    dateOfBirth: str
    gender: str
    phoneNum: str
    email: str
    localPlace: str
    points: int

def register_customer(customer_data):
    try:
        query = """
        INSERT INTO Customer (username, pasword, fname, lname, dateOfBirth, gender, phoneNum, email, localPlace, points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, customer_data)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@app.post('/register')
def register(new_customer: CustomerRegistration):
    try:
        customer_data = (
            new_customer.username,
            new_customer.pasword,
            new_customer.fname,
            new_customer.lname,
            datetime.strptime(new_customer.dateOfBirth, "%Y-%m-%d").date(),
            new_customer.gender,
            new_customer.phoneNum,
            new_customer.email,
            new_customer.localPlace,
            new_customer.points,
        )
        print(customer_data)
        register_customer(customer_data)
        return {"message": "Customer registered successfully"}
    except:
        raise HTTPException(status_code=500, detail="The username already used.")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)