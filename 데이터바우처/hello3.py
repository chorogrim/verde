import urllib3
import json

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"

accessKey = "706e5da0-3384-486d-b0d3-de90cae2053f"
analysisCode = "srl"
text = "획기적인 조형적 표현으로 때로는 하나의 조각작품처럼, 때로는 종교건물처럼 보이기도 하는 우리 동네의 상징적인 건축 작품입니다."

text += "특히 이 자유로운 곡선을 우리가 알고 있는 노출콘크리트 재료로 만들었다는 것이 놀랍습니다."
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
