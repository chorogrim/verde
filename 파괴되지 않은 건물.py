def solution(board, skill):
    n = len(board) # 보드의 행의 개수
    m = len(board[0]) # 보드의 열의 개수
    answer = n * m # 최초에 보드 전체의 칸 수를 답으로 초기화
    
    for type, r1, c1, r2, c2, degree in skill: # 주어진 스킬에 대해 반복
        for i in range(r1, r2+1): # 스킬의 영향이 미치는 행 범위에 대해 반복
            for j in range(c1, c2+1): # 스킬의 영향이 미치는 열 범위에 대해 반복
                if type == 1: # 스킬의 타입이 1인 경우
                    if 0 < board[i][j] <= degree: # 해당 칸의 값이 0보다 크고 스킬의 강도보다 작거나 같으면
                        answer -= 1 # 답에서 1을 빼서 해당 칸이 변화한 것으로 간주
                    board[i][j] -= degree # 해당 칸의 값에서 스킬의 강도를 뺌
                else: # 스킬의 타입이 2인 경우
                    if -degree < board[i][j] <= 0: # 해당 칸의 값이 0보다 작고 스킬의 강도의 반대 부호보다 크거나 같으면
                        answer += 1 # 답에 1을 더해서 해당 칸이 변화한 것으로 간주
                    board[i][j] += degree # 해당 칸의 값에 스킬의 강도를 더함
    return answer # 변화된 보드의 값들의 개수를 담은 변수를 반환