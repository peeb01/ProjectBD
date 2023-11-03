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
date of birth จะต้องอยู่ใน format ที่กำหนดให้ ตัวอย่างเช่น 1996-Jul-15 แบบนี้เท่านั้น 

gender จะต้องเป็น 1 ตัวอักษร คือ M, F

The masuerType field should be one of the following options:

- <span style="font-size: 12px;">นวดไทย</span>
- <span style="font-size: 12px;">นวดสวีเดน</span>
- <span style="font-size: 12px;">นวดเท้า</span>
- <span style="font-size: 12px;">นวดศีรษะ</span>
- <span style="font-size: 12px;">นวดกล้ามเนื้อคอ</span>
- <span style="font-size: 12px;">นวดรวม</span>
- <span style="font-size: 12px;">นวดเชียง</span>
- <span style="font-size: 12px;">นวดน้ำมันร้อน</span>
