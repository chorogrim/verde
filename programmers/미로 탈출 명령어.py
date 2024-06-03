from collections import deque

def check_condition(r,c,nr,nc,k,move_cnt): # 도착 지점까지 남은 거리와, 이동 가능한 횟수를 비교
   
    remain_cnt = abs(r-nr) + abs(c-nc) # 현재 위치에서 도착점까지의 거리를 계산
    possible_cnt = k-move_cnt # 현재까지의 이동 횟수를 기준으로 이동 가능한 횟수를 계산
 
    if possible_cnt < remain_cnt: # 이동 가능한 횟수가 남은 거리보다 작은 경우
        return False # 도착할 수 없으므로 False를 반환
    return True # 도착할 수 있는 경우에는 True를 반환

def bfs(n,m,x,y,r,c,k): # 총 행렬 크기와 시작점, 도착점, 이동 가능한 횟수를 인자로 받는 함수
    move_cnt = 0 # 이동 횟수 초기화
    route = "" # 이동 경로 초기화
    dq = deque() # BFS 탐색을 위한 큐 생성
    dq.append((x,y,move_cnt,route)) # 시작점r, 시작점c, 이동횟수, 이동 경로 큐에 추가

    while dq: # 큐가 비어있지 않은 동안 반복
        cr,cc,move_cnt,route = dq.popleft() # 큐에서 현재 위치, 이동 횟수, 이동 경로 가져옴
        # 도착 가능 여부 확인
        if (cr,cc)==(r,c):
            # 정확히 도착한 경우 -> 경로를 return
            if k == move_cnt:
                return route
            # 거리가 남는데 홀수인 경우 -> 도착 불가능, impossible을 return
            elif (k-move_cnt) %2 != 0:
                return "impossible"  
            
        # d,l,r,u 순서로 이동 
        for i in [1,2,3,0]:
            nr,nc = cr+dr[i], cc+dc[i]
            # 이동 가능 조건
            if not(0<nr<=n and 0<nc<=m) or move_cnt >= k or not check_condition(r,c,nr,nc,k,move_cnt+1): # 새로운 위치로 이동할 수 있는지 확인
                continue
            # 조건을 만족하는 경우 -> (d,l,r,u)로 이동하므로, 조건 만족하면 무조건 최단 경로임
            dq.append((nr,nc,move_cnt+1,route+moveDir[i])) # 새로운 위치와 이동 횟수, 이동 경로를 큐에 추가
            break # 조건을 만족하는 이동 방향이 발견되면 더 이상의 이동 방향을 탐색하지 않고 반복문을 종료
    return "impossible" # 최종적으로 도착 지점까지의 이동 경로를 방환 
            
def solution(n, m, x, y, r, c, k): # 주어진 파라미터를 인자로 받는 함수
    global graph, dr, dc, moveDir, remainDir # 전역 변수로 선언된 변수들을 함수 내에서 사용하기 위해 global 키워드로 선언
    graph = [[0]*(m+1) for _ in range(n+1)] # 주어진 행과 열 크기에 맞게 2차원 배열을 생성하고 0으로 초기화. 그래프를 표현하는 용도
    dr = [-1,1,0,0] # 상하좌우로 이동하기 위한 행의 변화량을 나타내는 리스트 
    dc = [0,0,-1,1] # 상하좌우로 이동하기 위한 열의 변화량을 나타내는 리스트
    moveDir = ['u','d','l','r'] # 상하좌우로 이동했을 때의 방향
    remainDir = ['ud', 'du', 'lr', 'rl'] # 남은 이동 방향을 나타내는 문자열
    # bfs 실행해서 최단경로를 탐색 
    return bfs(n,m,x,y,r,c,k) # 위에서 정의한 변수들을 활용하여 BFS 알고리즘을 실행하고, 최단 경로를 반환하는 함수를 호출하여 그 결과를 반환
