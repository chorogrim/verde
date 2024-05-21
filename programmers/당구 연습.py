# 시작점과 목표점이 주어졌을 때, 공이 벽에 부딪히는 경우 각 벽까지의 거리를 계산
def solve(x, y, startX, startY, ballX, ballY):
    dists = [] # 거리를 저장할 리스트
    # 위쪽 벽에 닿는 경우를 체크
    if not (ballX == startX and ballY > startY):
        d2 = (ballX - startX)**2 + (ballY - 2*y+startY)**2 # 공과 위쪽 벽 사이의 거리를 계산
        dists.append(d2) # 계산된 거리를 리스트에 추가
    # 아래쪽 벽
    # 단, x좌표가 같고 목표의 y가 더 작으면 안된다.
    if not (ballX == startX and ballY < startY):
        d2 = (ballX - startX)**2 + (ballY + startY)**2
        dists.append(d2)
    # 왼쪽 벽에 맞는 경우
    # 단, y좌표가 같고 목표의 x가 더 작으면 안된다.
    if not (ballY == startY and ballX < startX):
        d2 = (ballX + startX)**2 + (ballY - startY)**2
        dists.append(d2)
    # 오른쪽 벽
    # 단, y좌표가 같고 목표의 x가 더 크면 안된다.
    if not (ballY == startY and ballX > startX):
        d2 = (ballX - 2*x+startX)**2 + (ballY - startY)**2
        dists.append(d2)
    
    return min(dists)
    
def solution(m, n, startX, startY, balls):
    answer = []
    for ballX, ballY in balls:
        answer.append(solve(m, n, startX, startY, ballX, ballY))
    return answer # 모든 목표점들에 대한 거리가 담긴 리스트 반환