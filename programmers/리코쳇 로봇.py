def solution(board):
    que = [] # 탐색을 위한 큐를 빈 리스트로 초기화
    
    for x, row in enumerate(board): # board의 모든 위치를 탐색
        for y, each in enumerate(row):
            if board[x][y] == 'R':
                que.append((x, y, 0)) # 시작점을 찾으면 큐에 그 위치와 초기 거리를 (x, y, 0) 형태로 추가
    visited = set() # 방문한 위치를 저장할 집합 visited를 초기화
    
    while que: # 큐가 비어있지 않은 동안 반복
        x, y, length = que.pop(0) # 큐의 첫 번째 요소를 꺼내 (x, y, length)로 분해
        if (x, y) in visited: # (x, y)는 현재 위치, length는 시작점부터 현재 위치까지의 거리
            continue
            
        if board[x][y] == 'G': # (x, y)가 이미 방문된 적이 있으면 다음 반복으로 넘어감
            return length # 현재 위치의 값이 'G' 목표점이라면 현재까지의 거리 length를 반환
        visited.add((x, y)) # 현재 위치 (x, y)를 방문한 위치에 추가
        
        for diff_x, diff_y in ((0, 1), (0, -1), (1, 0), (-1, 0)): # 네방향(오른쪽, 왼쪽, 아래, 위)으로 이동하기 위한 좌표 변화를 diff_x, diff_y로 정의
            now_x, now_y = x, y 
            
            while True:
                next_x, next_y = now_x + diff_x, now_y + diff_y
                
                if 0 <= next_x < len(board) and 0 <= next_y < len(board[0]) and board[next_x][next_y] != 'D': # 현재 위치에서 시작하여 diff_x, diff_y만큼 이동한 다음 위치를 next_x, next_y로 계산
                    now_x, now_y = next_x, next_y
                    continue
                que.append((now_x, now_y, length + 1)) # 벽이나 보드의 경계에 도달하면, 이동을 멈추고 마지막 위치와 거리를 1 증가시켜 큐에 추가
                break
    return -1 # 큐가 비어있을 때까지 G에 도달하지 못하면, -1을 반환하여 경로가 없음을 나타냄 
