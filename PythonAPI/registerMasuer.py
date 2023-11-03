from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from datetime import date, datetime
from pydantic import BaseModel, Field
import pandas as pd

#-------------------------------------------------INITIALIZATION--------------------------------------------#


DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-M9VL3MH\SQLEXPRESS'
DATABASE_NAME = 'PP'
connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
app = FastAPI()




class MasuerRegistration(BaseModel):
    Id: int
    fname: str
    lname: str
    dateOfBirth: str
    gender: str
    phoneNum: str
    email: str
    masuerType: str
    dayoff: str

def register_masuer(masuer_data : tuple):
    data = cursor.execute("select * from Masuer").fetchall()
    Id = len(data) + 1
    try:
        query = """
        insert into Masuer (masuerId, fname, lname, dateOfBirth, gender, phoneNum, email, massuertype, dayoff, statusNow)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (Id,masuer_data))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@app.post('/register-masuer')
def register_masuer(new_masuer : MasuerRegistration):
    try:
        customer_data = (
            new_masuer.Id,
            new_masuer.fname,
            new_masuer.lname,
            datetime.strptime(new_masuer.dateOfBirth, "%Y-%m-%d").date(),
            new_masuer.gender,
            new_masuer.phoneNum,
            new_masuer.email,
            new_masuer.masuerType,
            new_masuer.dayoff
        )
        register_masuer(customer_data)
        return {"message": "Customer registered successfully"}
    except:
        raise HTTPException(status_code=500, detail="The username already used.")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
