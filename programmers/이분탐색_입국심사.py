def solution(n, times):
    '''
    n: 전체 인원 수
    times: 각 심사대의 처리 시간
    '''
    start = 1 # 최소 가능한 시간을 1초 초기화
    end = max(times) * n # 종료 시간을 설정
    
    while start <= end: # 시작 시간과 끝 시간이 같아질 때까지 반복
        mid = (start + end) // 2 # 중간 시간을 계산
        people = 0 # 현재 중간 시간에 해당하는 심사관들이 처리할 수 있는 총 인원 수를 초기화
        
        for t in times: # 각 심사관이 처리할 수 있는 인원 수를 계산
            people += mid // t # 중간시간을 해당 심사관의 처리 시간으로 나눈 몫을 더함
            
        if people >= n: # 처리된 총 인원이 목표 인원보다 크거나 같으면
            answer = mid # 현재 중간 시간을 답으로 저장
            end = mid - 1 # 끝 시간을 현재 중간 시간의 하나 작은 값으로 설정하여 범위를 좁힘
        else: # 처리된 총 인원이 목표 인원보다 작으면, 시작 시간을 조정
            start = mid + 1 # 시작 시간을 현재 중간 시간의 하나 큰 값으로 설정하여 범위를 좁힘
    return answer # 최종적으로 찾은 최소 시간을 반환
