from collections import deque

def check_condition(r,c,nr,nc,k,move_cnt):
    # 도착 지점까지 남은 거리와, 이동 가능한 횟수를 비교
    remain_cnt = abs(r-nr) + abs(c-nc)
    possible_cnt = k-move_cnt
    # 가능 횟수 < 남은 횟수 : false
    if possible_cnt < remain_cnt:
        return False
    # 가능 횟수 > 남은 횟수 : true
    return True

def bfs(n,m,x,y,r,c,k):
    move_cnt = 0
    route = ""
    dq = deque()
    dq.append((x,y,move_cnt,route)) # 시작점r, 시작점c, 이동횟수, 이동경로
    # 탐색 시작
    while dq:
        cr,cc,move_cnt,route = dq.popleft()
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
            if not(0<nr<=n and 0<nc<=m) or move_cnt >= k or not check_condition(r,c,nr,nc,k,move_cnt+1):
                continue
            # 조건을 만족하는 경우 -> (d,l,r,u)로 이동하므로, 조건 만족하면 무조건 최단 경로임
            dq.append((nr,nc,move_cnt+1,route+moveDir[i]))
            break
    return "impossible"
            
def solution(n, m, x, y, r, c, k):
    global graph, dr, dc, moveDir, remainDir
    graph = [[0]*(m+1) for _ in range(n+1)]
    dr = [-1,1,0,0]
    dc = [0,0,-1,1]
    moveDir = ['u','d','l','r']
    remainDir = ['ud', 'du', 'lr', 'rl']
    # bfs 실행해서 최단경로를 탐색
    return bfs(n,m,x,y,r,c,k)
