import urllib3
import json

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"

accessKey = "706e5da0-3384-486d-b0d3-de90cae2053f"
analysisCode = "dparse"
text = "건축가란 시간과 공간 속에 자신을 송두리째 불사르는 이들입니다."

text += "우리의 일상 속에 무심코 지나쳤을 수도 있는 그의 작품을 함께 둘러보며, 우리나라 현대 건축 여행을 떠나보실까요?"
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "text": text,
        "analysis_code": analysisCode
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))
