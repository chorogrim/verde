# 백준 문제 24479번 문제
# N개의 정점과 M개의 간선으로 구성된 무방향 그래프(undirected graph)가 주어진다.
# 정점 번호는 1번부터 N번이고 모든 간선의 가중치는 1이다.
# 정점 R에서 시작하여 깊이 우선 탐색으로 노드를 방문할 경우 노드의 방문 순서를 출력하자.
# 정점 1번에서 정점 2번을 방문한다. 정점 2번에서 정점 3번을 방문한다.
# 정점 3번에서 정점 4번을 방문한다.
# 정점 5번은 정점 1번에서 방문할 수 없다.


import sys

input = sys.stdin.readline
sys.setrecursionlimit(10**6) # 재귀 허용 깊이를 수동으로 늘려주는 코드

n, m, r = map(int, input().split()) # 입력받을 세개의 정수 선언(n = 정점의 개수, m = 간선의 개수, r = 시작 정점의 번호)
graph = [[] for _ in range(n+1)] # 빈 리스트를 요소로 갖는 리스트로 초기화. 각 인덱스는 정점을 나타내고, 해당 정점과 연결된 다른 정점들의 리스트를 저장
visited = [0] * (n+1) # 각 정점의 방문 여부를 나타내는 리스트로 초기화

for _ in range(m): # m번 반복하면서 각 간선에 대한 정보를 입력받음
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

def DFS(v, cnt): # 깊이 우선 탐색 시작
    visited[v] = cnt # 현재 정점 v와 현재까지 방문 순서 cnt를 인자로 받음

    # 방문 순서를 갱신하기 위해 tmp 값 이용
    tmp = 1
    # 현재 정점과 연결된 정점들을 방문 순서대로 정렬한 후 순회
    for adj_node in sorted(graph[v]):
        # 인접 정점이 방문되지 않았을 경우
        if not visited[adj_node]:
            # 해당 정점을 방문하고 재귀적으로 DFS 함수 호출
            tmp += DFS(adj_node, cnt+tmp)
    # tmp 값은 현재 정점을 루트로 하는 서브트리의 크기를 의미
    return tmp

# 정점의 방문 순서
DFS(r, 1)
# 줄바꿈 옵션 추가하여 방문 순서 출력(첫 번째 정점은 방문 순서에 포함시키지 않고, 나머지 정점들의 방문 순서를 출력)
print(*visited[1:], sep='\n')


