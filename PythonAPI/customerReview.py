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

class Reviews(BaseModel):
    username : str
    customerId : int
    reviewsText : str

@app.post('/reviews')
def cusReview(review: Reviews):
    username = review.username
    massuerId = review.customerId
    text = review.reviewsText
    ids = cursor.execute("select * from CustomerReview").fetchall()
    reviewId = len(ids) + 1
    current_time = datetime.now()
    try:
        query = """
                insert into CustomerReview(reviewId, username, masuerId, reviewText, dateTim)
                values (?, ?, ?, ?, ?)
                """

        cursor.execute(query, (reviewId, username, massuerId, text, current_time))
        conn.commit()

        return {"message": "Review inserted successfully"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
