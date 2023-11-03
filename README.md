# ProjectBD


# run at main.py

## Documentation run at http://localhost:8000/docs


# /register-masuer : method post
สำหรับ หมอนวดที่ต้องการสมัครเข้าทำงาน
โดยต้องการข้อมูลเป็นรูปแบบ JSON 

\```
Assistant: ```JSON
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