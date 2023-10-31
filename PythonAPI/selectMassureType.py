from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from datetime import date, datetime
from pydantic import BaseModel, Field
import pandas as pd
import json
#-------------------------------------------------INITIALIZATION--------------------------------------------#


DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-M9VL3MH\SQLEXPRESS'
DATABASE_NAME = 'PP'
connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
app = FastAPI()

class MassuerType(BaseModel):
    massuertype : str

def selectType(massuerType):
    try:
        query = """
                select M.fname, M.lname
                from Masuer M
                where M.massuertype = ?
                """
        cursor.execute(query, (massuerType.massuertype,))
        results = cursor.fetchall()
        print(results)
        dict_list = [{'First Name': item[0], 'Last Name': item[1]} for item in results]
        results_json = json.dumps(dict_list, ensure_ascii=False, indent=2)
        return results_json
    except Exception as e:
        return str(e)

@app.post("/main/massuertype")
async def massuertype(mtype: MassuerType):
    try:
        results = selectType(mtype)
        return results
    except:
        raise HTTPException(status_code=500, detail="Nothing.")
    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
