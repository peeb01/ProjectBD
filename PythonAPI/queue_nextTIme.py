from fastapi import FastAPI, HTTPException
import pyodbc
import uvicorn
from datetime import date, datetime
from pydantic import BaseModel, Field
import pandas as pd
import json

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-M9VL3MH\SQLEXPRESS'
DATABASE_NAME = 'PP'
connection_string = f"DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"


conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
app = FastAPI()


class selectDay(BaseModel):
    dateTimes : str
    massuertype : str

@app.post("/main/massuertype/selectnexttime")
async def select_next_time(select_day: selectDay):
    input_date_str = select_day.dateTimes
    massuertype = select_day.massuertype

    input_date = datetime.strptime(input_date_str, "%Y-%b-%d")

    day_of_week = input_date.strftime("%A")
    query = """
            select M.masuerId, M.fname, M.lname
            from Masuer M
            where M.dayoff <> ? and M.massuertype = ? and M.statusNow = 1
            """

    cursor.execute(query, (day_of_week, massuertype))
    result = cursor.fetchall()
    dict_list = [{'ID': item[0],'First Name': item[1], 'Last Name': item[2]} for item in result]
    results_json = json.dumps(dict_list, ensure_ascii=False, indent=3)
    return results_json

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
