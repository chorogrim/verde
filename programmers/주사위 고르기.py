def solution(h1, m1, s1, h2, m2, s2): # 시작 시간과 종료 시간을 받는 함수
    answer = 0 # 만나는 횟수 저장할 변수 초기화

    # 시작시간과 끝시간을 초단위로 변환
    startTime = h1 * 3600 + m1 * 60 + s1 # 시작 시간을 초 단위로 계산
    endTime = h2 * 3600 + m2 * 60 + s2 # 종료 시간을 초 단위로 계산

    if startTime == 0 * 3600 or startTime == 12 * 3600: # 시작 시간이 0시(12시)인 경우 카운팅에 포함
        answer += 1

    while startTime < endTime: # 시작 시간부터 종료 시간까지 반복
        hCurAngle = startTime / 120 % 360 # 시침의 현재 각도 계산
        mCurAngle = startTime / 10 % 360 # 분침의 현재 각도 계산
        sCurAngle = startTime * 6 % 360 # 초침의 현재 각도 계산

        hNextAngle = 360 if (startTime + 1) / 120 % 360 == 0 else (startTime + 1) / 120 % 360 # 다음 초의 시침의 각도 계산
        mNextAngle = 360 if (startTime + 1) / 10 % 360 == 0 else (startTime + 1) / 10 % 360 # 다음 초의 분침의 각도 계산
        sNextAngle = 360 if (startTime + 1) * 6 % 360 == 0 else (startTime + 1) * 6 % 360 # 다음 초의 초침의 각도 계산

        if sCurAngle < hCurAngle and sNextAngle >= hNextAngle: # 초침이 시침과 만나는 경우 카운팅
            answer += 1
        if sCurAngle < mCurAngle and sNextAngle >= mNextAngle: # 초침이 분침과 만나는 경우 카운팅
            answer += 1
        if sNextAngle == hNextAngle and hNextAngle == mNextAngle: # 시침,분침이 동시에 겹쳤을 때 중복 카운팅 제외 
            answer -= 1

        startTime += 1 # 시작 시간을 1초씩 증가시키며 반복 진행
    
    return answer # 최종적으로 만나는 횟수 반환
