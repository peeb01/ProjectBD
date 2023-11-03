# ProjectBD

# ยังไม่ได้เปิด port ให้เชื่อมต่อ
### run at main.py

### Documentation run at http://localhost:8000/docs


## /register-masuer (Method: POST)



```JSON
{
  "fname": "string",
  "lname": "string",
  "dateOfBirth": "string",
  "gender": "string",
  "phoneNum": "string",
  "email": "string",
  "masuerType": "string",
  "dayoff": "string"
}
```
The date of birth should be in the specified format, for example:

- 1996-Jul-15
- 2004-Sep-19
- 1990-May-28

The gender should be a single character, either:

- M
- F


The masuerType field should be one of the following options:

- นวดไทย
- นวดสวีเดน
- นวดเท้า
- นวดศีรษะ
- นวดกล้ามเนื้อคอ
- นวดรวม
- นวดเชียง
- นวดน้ำมันร้อน

Day off is all day in the week:

- Monday
- Tuesday
- Wednesday
- Thursday
- Friday
- Saturday


## /register (Method: POST)

```JSON
{
  "username": "string",
  "pasword": "string",
  "fname": "string",
  "lname": "string",
  "dateOfBirth": "string",
  "gender": "string",
  "phoneNum": "string",
  "email": "string",
  "localPlace": "string"
}
```
The data input like register-masuer


## /login (Method: POST)
```JSON
{
  "username": "string",
  "password": "string"
}
```

## /login-masuer (Method: POST)
```JSON
{
  "Id": "integer",
  "masuerName": "string"
}
```

## /main (Method: GET)
Will return all Masuer already to Massage Now

## /main/massuertype (Method: POST)
After /main the Customer will select Type for them, this will return All Masuer Already now and Masuer have type a Customer wants.
```JSON
{
  "massuertype": "string"
}
```
The masuerType field should be one of the following options:

- นวดไทย
- นวดสวีเดน
- นวดเท้า
- นวดศีรษะ
- นวดกล้ามเนื้อคอ
- นวดรวม
- นวดเชียง
- นวดน้ำมันร้อน

## /main/massuertype/selectnexttime (Method: POST)
To select next time if Customer want will return masuer already in the time.
```JSON
{
  "dateTimes": "string",
  "massuertype": "string"
}
```
Date Time format Example: 
- 2023-Nov-30

The masuerType field should be one of the following options:

- นวดไทย
- นวดสวีเดน
- นวดเท้า
- นวดศีรษะ
- นวดกล้ามเนื้อคอ
- นวดรวม
- นวดเชียง
- นวดน้ำมันร้อน

## /main/massuertype/selectnexttime/book-appointment (Method: POST)
To Booking masuer for masage  
```JSON
{
  "username": "string",
  "masuerId": "int",
  "masuerFName": "string",
  "masuerLName": "string",
  "timewant": "int",
  "time_bookingwant": "string"
}
```
timewant format is minutes example:
- 30
- 60
- 120

time_bookingwant format example:
- 2023-Nov-9 15-00-00

## /main/massuerscheduling (Method: POST)
the masuer wii see Scheduling table of them.
```JSON
{
  "massuerId": "integer"
}
```

## /massuerIncome (Methed: GET)
To see all in come when masuer masage will got money from customer. but all day 1 of month start count from Machine Time.


## /reviews (Method: POST)
Customer will review Masuer after masage.
```JSON
{
  "username": "string",
  "customerId": 0,
  "reviewsText": "string"
}
```
