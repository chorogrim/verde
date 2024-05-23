def solution(today, terms, privacies):
    answer = []
    today = list(map(int, today.split('.'))) # 문자열을 '.' 기준으로 분리한 후, 각 부분을 정수형 리스트로 변환
    today = today[2] + today[1] * 28 + today[0] * 28 * 12 # today를 '년.월.일' 형식에서 일로 변환

    dic = {} # 각 개인정보 보유 기간을 저장할 사전을 초기화
    for data in terms: # terms 리스트의 각 항목에 대해 반복
        code, month = data.split(" ") # 각 항목을 코드와 기간으로 분리 
        dic[code] = int(month) * 28 # 기간을 월 단위로 변환한 후, 사전에 저장

    for i in range(len(privacies)): # privacires 리스트의 각 항목에 대해 인덱스를 이용하여 반복
        day, code = privacies[i].split() # 각 항목을 날짜와 코드로 분리 
        day = list(map(int, day.split('.'))) # day 문자열을 '.'기준으로 분리한 후, 각 부분을 정수형 리스트로 변환
        day = day[2] + day[1] * 28 + day[0] * 28 * 12 # 일 단위로 변환
        if day + dic[code] <= today: # 개인정보 저장 날짜에 해당 코드의 유효 기간을 더한 값이 오늘 날짜보다 작거나 같으면, 만료된 것으로 간주
            answer.append(i + 1) # 만료된 개인정보의 인덱스를 결과 리스트에 추가

    return answer  # 만료된 개인 정보 인덱스 리스트를 반환
