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
date of birth จะต้องอยู่ใน format ที่กำหนดให้ ตัวอย่างเช่น:

-1996-Jul-15
-2004-Sep-19
-1990-May-28




gender จะต้องเป็น 1 ตัวอักษร คือ:

-M
-F


The masuerType field should be one of the following options:

- นวดไทย
- นวดสวีเดน
- นวดเท้า
- นวดศีรษะ
- นวดกล้ามเนื้อคอ
- นวดรวม
- นวดเชียง
- นวดน้ำมันร้อน

