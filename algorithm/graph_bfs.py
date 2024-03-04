# 백준 14940번 문제
# 지도가 주어지면 모든 지점에 대해서 목표지점까지의 거리를 구하여라.
# 문제를 쉽게 만들기 위해 오직 가로와 세로로만 움직일 수 있다고 하자.
# 지도의 크기 n과 m이 주어진다. n은 세로의 크기, m은 가로의 크기다.(2 ≤ n ≤ 1000, 2 ≤ m ≤ 1000)
# 다음 n개의 줄에 m개의 숫자가 주어진다. 0은 갈 수 없는 땅이고 1은 갈 수 있는 땅, 2는 목표지점이다. 입력에서 2는 단 한개이다.


import sys
from collections import deque

# 시작 지점 (x_start,y_start)에서부터 BFS 탐색 시작
def bfs(x_start,y_start):
    # BFS 탐색을 위한 큐 생성
    queue=deque()
    # 시작점에 큐 추가
    queue.append([x_start,y_start])

    # 큐가 비어있지 않은 동안에 아래의 동작을 반복
    while queue:
        # 큐의 맨 앞에서 좌표 하나를 꺼냄
        x, y = queue.popleft()

        # 현재 위치에서 상하좌우로 이동할 수 있는지 확인하기 위해 상하좌우 4방향 탐색
        for i in range(4):
            # 현재 위치에서 상하좌우로 이동한 새로운 좌표를 계산
            nx = x + dx[i]
            ny = y + dy[i]

            # 새로운 좌표가 미로의 범위를 벗어나면 다음 반복으로 넘어감
            if nx<0 or nx>=n or ny<0 or ny >=m:
                continue
           
            # 새로운 좌표가 이미 방문한 곳이라면 다음 반복으로 넘어감
            if answer[nx][ny]!= -1:
                continue

            # 새로운 좌표까지의 최단 거리를 현재 위치까지의 거리에 1을 더한 값으로 업데이트
            answer[nx][ny]=answer[x][y]+1
            # 새로운 좌표를 큐에 추가하여 다음 탐색을 위해 준비
            queue.append([nx,ny])

# 미로의 세로와 가로 크기. n과 m을 입력받기
n, m = map(int, sys.stdin.readline().split()) 
# 상하좌우 이동을 나타내는 배열
dx = [-1,0,1,0] # 상하 이동에 대한 값을 저장
dy = [0,1,0,-1] # 좌우 이동에 대한 값을 저장

# 미로 정보 저장. 2차원 배열을 나타내는 리스트
myMap = []
for i in range(n):
    # 입력으로 받은 한 줄을 공백을 기준으로 분리하여 정수형으로 변환한 리스트를 만듦
    myMap.append(list(map(int,sys.stdin.readline().split())))

# BFS를 수행한 결과인 각 칸까지의 최단거리 저장
answer = []
# 0은 시작 지점(x_start, y_start)을 초기화
x_start, y_start = 0,0 
# n번만큼 반복하여 2차원 배열의 각 행에 대해 아래의 동작을 수행
for i in range(n):
    # answer 리스트에 빈 리스트 추가
    answer.append([])
    # 각 열에 대해 아래의 동작을 수행
    for j in range(m):
        # 시작 지점을 나타내는 숫자인 2라면,
        if myMap[i][j] == 2: 
            # 시작 지점의 좌표를(i, j)로 갱신하고
            x_start, y_start = i, j 
            # 해당 위치의 answer 값을 0으로 초기화
            answer[i].append(0)
        # 벽을 나타내는 숫자인 1이라면,
        elif myMap[i][j] == 1: 
            # 해당 위치의 answer 값을 -1로 초기화
            answer[i].append(-1)
        # 둘 다 아니라면 answer 값을 0으로 초기화
        else: 
            answer[i].append(0)

# BFS를 시작 지점에서 호출하여 각 칸까지의 최단 거리를 계산
bfs(x_start,y_start)

# n번 만큼 반복하여
for i in range(n):
    # m번 만큼 반복하여
    for j in range(m):
        # 출력시 공백으로 구분하여 한 줄에 출력
        print(answer[i][j], end=' ')
    print()
