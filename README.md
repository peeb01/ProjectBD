# ProjectBD


### run at main.py

### Documentation run at http://localhost:8000/docs


## Endpoint: /register-masuer (Method: POST)


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


## Endpoint: /register (Method: POST)

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


## Endpoint: /login (Method: POST)
```JSON
{
  "username": "string",
  "password": "string"
}
```

## Endpoint: /login-masuer (Method: POST)
```JSON
{
  "Id": "integer",
  "masuerName": "string"
}
```

## Endpoint: /main (Method: GET)
Will return all Masuer already to Massage Now

## Endpoint: /main/massuertype (Method: POST)
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

## Endpoint:  /main/massuertype/selectnexttime (Method: POST)
To select next time if Customer want will return masuer already in the time.
```JSON
{
  "dateTimes": "string",
  "massuertype": "string"
}
```
Date Time format Example: 
-2023-Nov-30

The masuerType field should be one of the following options:

- นวดไทย
- นวดสวีเดน
- นวดเท้า
- นวดศีรษะ
- นวดกล้ามเนื้อคอ
- นวดรวม
- นวดเชียง
- นวดน้ำมันร้อน


