import subprocess

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



#--------------------------------------------------REGISTER-------------------------------------------------#
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

def register_customer(customer_data : tuple):
    """
    This function use for Register query into database
    
    Args :
        the data for input             
        (
        username    : str,
        password    : str,
        fname       : str,     
        lname       : str,
        dateOfBirth : str --> convert to datetime datetime.strptime(dateOfBirth, "%Y-%m-%d").date(),
        gender      : str,
        phoneNum    : str,
        email       : str,
        localOlace  : str,
        points      : int               
        )
    """
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
def register(new_customer : CustomerRegistration):
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
        register_customer(customer_data)
        return {"message": "Customer registered successfully"}
    except:
        raise HTTPException(status_code=500, detail="The username already used.")



#----------------------------------------------------LOGIN----------------------------------------------#
class UserCredentials(BaseModel):
    username: str
    password: str


def verify_credentials(username: str, password: str) -> bool:
    """
    function use for check username and password in database 

    Args :
        username : str,
        password : str

    Returns : Boolean if true login sucsesfull
    """
    try:

        query = "SELECT COUNT(*) FROM Customer WHERE username = ? AND pasword = ?"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return result[0] > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/login")
async def login(credentials: UserCredentials):
    if verify_credentials(credentials.username, credentials.password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


#---------------------------------------------------- MAIN PAGE --------------------------------------------------#
import json

def selectMasuer():
    try:
        query = """
                select M.fname, M.lname, M.gender, M.massuertype
                from Masuer M
                where ( M.dayoff <> (select datename(weekday, getdate()) as CurrentDayOfWeek)) and (M.statusNow = 1) 
                """      
        cursor.execute(query)
        results = cursor.fetchall()
        # print(results)
        # df = pd.DataFrame(results, columns=['fname', 'lname', 'gender', 'massuertype'])
        # result_json = df.to_json(orient='index')

        dict_list = [{'First Name': item[0], 'Last Name': item[1], 'Gender': item[2], 'Massage Type': item[3]} for item in results]
        result_json = json.dumps(dict_list, ensure_ascii=False, indent=4)
        return result_json
    except Exception as e:
        return str(e)

@app.get("/main")
async def main():
    try:
        result_json = selectMasuer() 
        return result_json
    except Exception as e:
        return {"error": str(e)}


#------------------------------------------------- SELECT MASSUER TYPE ---------------------------------------#
class MassuerType(BaseModel):
    massuertype : str

def selectType(massuerType):
    try:
        query = """
                select M.fname, M.lname
                from Masuer M
                where M.massuertype = ?
                """
        cursor.execute(query, (massuerType.massuertype,))  # You should pass a tuple as a parameter
        results = cursor.fetchall()
        print(results)
        dict_list = [{'First Name': item[0], 'Last Name': item[1]} for item in results]
        results_json = json.dumps(dict_list, ensure_ascii=False, indent=2)
        return results_json
    except Exception as e:
        return str(e)

# Your route handler
@app.post("/main/massuertype")
async def massuertype(mtype: MassuerType):
    try:
        results = selectType(mtype)
        return results
    except:
        raise HTTPException(status_code=500, detail="Nothing.")
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

