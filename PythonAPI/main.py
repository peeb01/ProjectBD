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


#-------------------------------------------------Masuer register -----------------------------------------#
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

#--------------------------------------------------Masuer Login---------------------------------------------------#

class MasuerCredentials(BaseModel):
    Id: int
    masuerName : str

def verify_masuer(Id: str, masuerName: str) -> bool:
    """
    function use for check username and password in database 

    Args :
        Id : str,
        masuerName : str

    Returns : Boolean if true login sucsesfull
    """
    try:

        query = "select count(*) from Masuer where masuerId = ? and fname = ?"
        cursor.execute(query, (Id, masuerName))
        result = cursor.fetchone()
        return result[0] > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/login-masuer")
async def loginMasuer(credentials: MasuerCredentials):
    if verify_masuer(credentials.Id, credentials.masuerName):
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
    
#------------------------------------------------- Queue and next Time -------------------------------------------------------#
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

#-------------------------------------------- Buy, Booking -----------------------------------------#
from datetime import timedelta

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

    current_time = datetime.now()
    
    if timebookwill <= current_time:
        return {"message": "Booking time must be after the current time."}

    timeout = timebookwill + timedelta(minutes=timewant)

    try:
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Check if existing bookings with the same masuerId and overlapping time periods
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
                insert into Booking (bookingId, username, masuerID, massuertype, datTime, Timemasuer, Timeofout)
                values (?, ?, ?, ?, ?, ?, ?)
                """
        cursor.execute(query, (bookingId, username, masuerId, f"{masuerFName} {masuerLName}", current_time_str, timebookwill, timeout))
        
        conn.commit()

        return {"message": "Appointment booked successfully"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

#--------------------------------------------------Massuer Scheduling------------------------------------------#
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


#------------------------------------------------- Massuer Income ---------------------------------------------#

def getMassuerIncome():
    try:
        qeury = """
                select B.masuerID, B.massuerName, sum(B.prices) as TotalPrices
                from Booking B
                where B.Timemasuer >= dateadd(month, datediff(month, 0, getdate()), 0)
                group by B.masuerID, B.massuerName
                """
        cursor.execute(qeury)
        results = cursor.fetchall()
        
        dict_list = [{'Masuer ID': item[0],'Masuer Name': item[1], 'Total income': item[2]} for item in results]
        results_json = json.dumps(dict_list, ensure_ascii=False, indent=3)
        return results_json   

    except Exception as e:
        return str(e)

@app.get('/massuerIncome')
async def massuerIncome():
    try:
        result_json = getMassuerIncome()
        return result_json
    except Exception as e:
        return {"error": str(e)}
    
#------------------------------------------------- Massuer Salary ---------------------------------------------#

def getMassuerSalary():
    try:
        qeury = """
                select B.masuerID, B.massuerName, (sum(B.prices))*0.75 as TotalPrices
                from Booking B
                where B.datTime >= dateadd(month, datediff(month, 0, getdate()), 0)
                group by B.Timemasuer, B.massuerName
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


#------------------------------------------------- Customer Review ---------------------------------------------#

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
    uvicorn.run("main:app", host="192.168.3.2", port=80)  # host is IPv4 of computer
