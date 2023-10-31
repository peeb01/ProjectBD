from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from datetime import date, datetime
from pydantic import BaseModel, Field
import pandas as pd
import json
from datetime import timedelta


DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-M9VL3MH\SQLEXPRESS'
DATABASE_NAME = 'PP'
connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
app = FastAPI()

def getMassuerSalary():
    try:
        qeury = """
                select B.masuerID, B.massuerName, (sum(B.prices))*0.75 as TotalPrices
                from Booking B
                where B.datTime >= dateadd(month, datediff(month, 0, getdate()), 0)
                group by B.masuerID, B.massuerName
                """
        cursor.execute(qeury)
        results = cursor.fetchall()
        
        dict_list = [{'Masuer ID': item[0],'Masuer Name': item[1], 'Total income': item[2]} for item in results]
        results_json = json.dumps(dict_list, ensure_ascii=False, indent=3)
        return results_json   
    except Exception as e:
        return str(e)

@app.get('/massuerSalary')
async def massuerSalary():
    try:
        result_json = getMassuerSalary()
        return result_json
    except Exception as e:
        return {"error": str(e)} 


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
