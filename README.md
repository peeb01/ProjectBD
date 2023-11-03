# ProjectBD


# run at main.py

## Documentation run at http://localhost:8000/docs


#### /register-masuer : method post

\```
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
``` text 
date of birth จะต้องอยู่ใน format ที่กำหนดให้ ตัวอย่างเช่น 1996-Jul-15 แบบนี้เท่านั้น 
gender จะต้องเป็น 1 ตัวอักษร คือ M, F
masuerType มีให้เลือก 
--"นวดไทย", 
--"นวดสวีเดน", 
--"นวดเท้า", 
--"นวดศีรษะ", 
--"นวดกล้ามเนื้อคอ", 
--"นวดรวม",
--"นวดเชียง",
--"นวดน้ำมันร้อน"