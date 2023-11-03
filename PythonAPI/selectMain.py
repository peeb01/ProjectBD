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


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
