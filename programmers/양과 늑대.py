def solution(a, b, g, s, w, t):
    '''
    a: 목표 금
    b: 목표 은
    g: 금의 양
    s: 은의 양
    w: 트럭의 최대 운반량
    t: 편도 이동 시간
    '''
    left = 0 # 이진 탐색의 좌측 경계값 설정
    right = (10**14*2-1) + (10**14*2-1) # 이진 탐색의 우측 경계값 설정
    result = right # 결과를 저장할 변수를 초기화

    while left <= right: # 이진 탐색 시작
        mid = (left + right) // 2 # 중간 값 계산
        gold, silver, total = 0, 0, 0 # 중간 값 mid 시간 내에 운반할 수 있는 금, 은, 총량을 저장할 변수 초기화

        for i in range(len(t)): # 각 트럭에 대해 반복
            cnt = (mid // (t[i]*2)) # 왕복하는데 걸리는 시간으로 트럭이 왕복할 수 있는 횟수를 계산
            cnt += 1 if mid % (t[i]*2) >= t[i] else 0 # 마지막 편도 운행을 고려하여 운행 횟수를 보정

            gold += min(g[i], cnt*w[i]) # 현재 트럭이 운반할 수 있는 금의 최대량을 추가
            silver += min(s[i], cnt*w[i]) # 현재 트럭이 운반할 수 있는 은의 최대량을 추가
            total += min(g[i] + s[i], cnt*w[i]) # 현재 트럭이 운반할 수 있는 금과 은의 총량을 추가

        if gold >= a and silver >= b and total >= a+b: # 필요한 금과 은의 양을 만족하는지 확인
            right = mid - 1 # 만족하면 더 작은 시간을 찾기 위해 우측 경계를 줄임
            result = min(mid, result) # 현재 mid 값을 결과에 저장
        else: # 필요한 금과 은의 양을 만족하지 못하면
            left = mid + 1 # 더 큰 시간을 찾기 위해 좌측 경계를 늘림
    return result # 최종적으로 찾은 최소 시간을 반환