# 백준 1260번 문제
# 그래프를 DFS로 탐색한 결과와 BFS로 탐색한 결과를 출력하는 프로그램을 작성하시오.
# 단, 방문할 수 있는 정점이 여러 개인 경우에는 정점 번호가 작은 것을 먼저 방문하고, 더 이상 방문할 수 있는 점이 없는 경우 종료한다. 
# 정점 번호는 1번부터 N번까지이다.


from collections import deque

# 정점, 간선수, 시작점을 입력받음
n, m, v = map(int, input().split())
# 초기값을 False로 만들어 그래프를 선언
# n+1 개의 행과 열을 가진 이차원 리스트를 생성
# False로 초기화된 이차원 리스트를 만드는데, 각 요소는 해당 위치의 정점과 다른 정점 간에 간선이 있는지 여부를 나타냄
graph = [[False] * (n+1) for _ in range(n+1)]

# m번 반복하면서
for i in range(m) :
    # 각 반복에서는 사용자로부터 두개의 정수를 입력받음
    x, y = map(int, input().split())
    # 변환된 두 정수를 각각 x, y 변수에 할당. 그래프의 간선 정보를 나타내는 인접 형렬에 해당 간선의 존재를 표시
    graph[x][y] = 1
    graph[y][x] = 1

# dfs와 bfs 그래프의 방문 여부를 담을 리스트
visited1 = [False] * (n+1) # 정점의 방문 여부를 나타냄
visited2 = [False] * (n+1) # 정점을 방문하지 않은 상태로 설정

# 깊이 우선 탐색을 수행하는 함수. 시작 정점 v를 인자로 받음
def dfs(v):
    # 정점 v를 방문했음을 표시하기 위해 인덱스를 True로 설정 (방문 처리)
    visited1[v] = True
    # 방문 후, 정점 출력
    print(v, end=" ")
    # 모든 정점을 순회
    # 방문기록이 없고, 인덱스에 값이 있다면(연결되어 있다면)   
    for i in range(1, n + 1):
        if not visited1[i] and graph[v][i] == 1:
       # 호출될 때마다 visted는 1이되고  재귀되어 v에 i가 들어감
            dfs(i)

# 너비 우선 탐색을 수행하는 함수. 시작 정점 v를 인자로 받음
def bfs(v):
    # 방문할 곳을 순서대로 넣을 큐
    q = deque([v])
    # 방문 처리
    visited2[v] = True
    # 큐 안에 데이터가 없을 때 까지 실행됨
    while q:
    # 큐 맨 앞에 있는 값을 꺼내서 출력
        v = q.popleft()
        print(v, end=" ")
        for i in range(1, n + 1):
            # 방문기록이 없고, 인덱스에 값이 있다면(연결되어 있다면)
            if not visited2[i] and graph[v][i] == 1:
                q.append(i) # 큐에 추가
                visited2[i] = True # 정점 방문 처리
dfs(v) # 깊이 우선 탐색을 호출하는 부분
print() # dfs 결과 출력 후 줄바꿈을 위한 출력
bfs(v) # bfs를 호출하는 부분