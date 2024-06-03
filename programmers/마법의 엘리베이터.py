def solution(storey): # 주어진 층수를 인자로 받는 함수
    answer = [] # 가능한 모든 경우의 이동 횟수를 저장할 리스트
    
    def dfs(st, count): # 깊이 우선 탐색을 수행하는 내부 함수
        '''
        st: 현재 층수
        count: 이동 횟수
        '''
        if st == 0: # 만약 현재 층수가 0이라면, 목표 층수에 도착했다면
            answer.append(count) # 이동 횟수를 answer 리스트에 추가
            return # 함수 종료
        
        one = st % 10 # 현재 층수의 일의 자리 숫자를 구함
        up, down = 10 - one, one # 올라가거나 내려가는 경우의 이동 횟수를 계산
        
        if up < down: # 위로 올라가는 경우가 아래로 내려가는 경우보다 이동 횟수가 적을 때
            dfs(st // 10 + 1, count + up) # 다음 층수로 이동하고, 이동 횟수를 업데이트하여 재귀적으로 호출
        elif down < up: # 아래로 내려가는 경우가 위로 올라가는 경우보다 이동 횟수가 적을 때
            dfs(st //10, count + down) # 다음 층수로 이동하고, 이동 횟수를 업데이트하여 재귀적으로 호출
        else: # 위로 올라가는 경우와 아래로 내려가는 경우의 이동 횟수가 같은 경우
            for i in range(2): # 두 가지 모두를 고려하여 반복
                dfs(st // 10 + i, count + up) # 다음 층수로 이동하고, 이동 횟수를 업데이트하여 재귀적으로 호출
    
    dfs(storey, 0) # dfs 함수를 시작점과 초기 이동 횟수 0으로 호출하여 탐색을 시작
    return min(answer) # 가능한 모든 경우의 이동 횟수 중 최소값을 반환
