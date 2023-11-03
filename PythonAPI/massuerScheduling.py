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

class MassuerScheduiling(BaseModel):
    massuerId : int

@app.post("/main/massuerscheduling")
def selectMasuerScheduling(massuer: MassuerScheduiling):
    msuerId = massuer.massuerId

    current_time = datetime.now()

    query = """
            select M.fname, M.lname, C.fname, B.Timemasuer
            from Customer C, Masuer M, Booking B
            where (B.username = C.username) and (M.masuerId = B.masuerID) and (B.masuerID = ?) and (B.Timemasuer >= ?)
            """
    cursor.execute(query, (msuerId, current_time))
    result = cursor.fetchall()
    dict_list = [{'Masuer firstname': item[0], 'Masuer lastname': item[1], 'Customer name': item[2], 'start Time': item[3]} for item in result]

    # Convert datetime to strings
    for item in dict_list:
        item['start Time'] = item['start Time'].isoformat()

    # Sort the results by 'start Time' 
    sorted_dict_list = sorted(dict_list, key=lambda item: item['start Time'])

    results_json = json.dumps(sorted_dict_list, ensure_ascii=False, indent=4)
    return results_json


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
