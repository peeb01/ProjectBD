# ProjectBD


# run at main.py

## Documentation run at http://localhost:8000/docs


### Endpoint: /register-masuer (Method: POST)


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

<span style="background-color: red;">The dateOfBirth field should be in the specified format, for example, "1996-Jul-15."</span>

<span style="background-color: red;">The gender field should be a single character, either "M" for male or "F" for female.</span>

<span style="background-color: red;">The masuerType field should be one of the following options:</span>

"นวดไทย"
"นวดสวีเดน"
"นวดเท้า"
"นวดศีรษะ"
"นวดกล้ามเนื้อคอ"
"นวดรวม"
"นวดเชียง"
"นวดน้ำมันร้อน"