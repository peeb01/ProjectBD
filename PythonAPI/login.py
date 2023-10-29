from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from pydantic import BaseModel

class UserCredentials(BaseModel):
    username: str
    password: str

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-M9VL3MH\SQLEXPRESS'
DATABASE_NAME = 'PP'

connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
app = FastAPI()

def verify_credentials(username: str, password: str) -> bool:
    """
    function use for check username and password in database 

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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

## ควยปัน