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




class init_buy(BaseModel):
    username : str
    masuerId : int
    masuerFName : str
    masuerLName : str
    timewant : int      # minutes
    time_bookingwant : str


@app.post("/main/massuertype/selectnexttime/book-appointment")
async def book_appointment(booking_info: init_buy):

    username = booking_info.username
    masuerId = booking_info.masuerId
    masuerFName = booking_info.masuerFName
    masuerLName = booking_info.masuerLName
    timewant = booking_info.timewant
    timebookwill = datetime.strptime(booking_info.time_bookingwant, "%Y-%b-%d %H-%M-%S")
    execute_cursor = cursor.execute("select * from Booking").fetchall()
    bookingId = len(execute_cursor) + 1

    points = timewant
    if timewant < 30:
        return{"message": "Only bookings of more than 30 minutes are allowed."}
    current_time = datetime.now()
    
    if timebookwill <= current_time:
        return {"message": "Booking time must be after the current time."}

    timeout = timebookwill + timedelta(minutes=timewant)
    prices = timewant * 10
    try:
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Check if there are any existing bookings with the same masuerId and overlapping time periods
        conflict_query = """
                        select count(*) from Booking
                        where masuerID = ? and
                              (Timeofout >= ? and Timemasuer <= ?)
                        """
        conflict_count = cursor.execute(conflict_query, (masuerId, timebookwill, timeout)).fetchone()[0]

        if conflict_count > 0:
            return {"message": "Booking conflicts with an existing appointment for the same masuerId."}

        # Fetch the current points from the Customer table
        points_query = "select points from Customer where username = ?"
        current_points = cursor.execute(points_query, username).fetchone()[0]
        
        # Calculate new points
        new_points = current_points + points
        # Update the points in the Customer table
        update_point = """
                update Customer
                set points = ?
                where username = ?
                """
        cursor.execute(update_point, (new_points, username))
        
        # Insert the booking into the database
        query = """
                insert into Booking (bookingId, username, masuerID, massuerName, datTime, Timemasuer, Timeofout, prices)
                values (?, ?, ?, ?, ?, ?, ?, ?)
                """
        cursor.execute(query, (bookingId, username, masuerId, f"{masuerFName} {masuerLName}", current_time_str, timebookwill, timeout, prices))
        
        conn.commit()

        return {"message": "Appointment booked successfully"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
