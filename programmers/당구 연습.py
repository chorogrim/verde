# 시작점과 목표점이 주어졌을 때, 공이 벽에 부딪히는 경우 각 벽까지의 거리를 계산
def solve(x, y, startX, startY, ballX, ballY):
    dists = [] # 거리를 저장할 리스트
    
    # 위쪽 벽에 닿는 경우를 체크
    if not (ballX == startX and ballY > startY): # 만약 공의 x좌표가 시작점과 같지 않고, 공의 y좌표가 시작점의 y좌표보다 크지 않은 경우를 체크
        d2 = (ballX - startX)**2 + (ballY - 2*y+startY)**2 # 공과 위쪽 벽 사이의 거리를 계산
        dists.append(d2) # 계산된 거리를 리스트에 추가
        
    # 아래쪽 벽
    # 단, x좌표가 같고 목표의 y가 더 작으면 안됨
    if not (ballX == startX and ballY < startY):
        d2 = (ballX - startX)**2 + (ballY + startY)**2 # 공과 위쪽 벽 사이의 거리를 계산
        dists.append(d2) # 계산된 거리를 리스트에 추가
        
    # 왼쪽 벽에 맞는 경우
    # 단, y좌표가 같고 목표의 x가 더 작으면 안됨
    if not (ballY == startY and ballX < startX): 
        d2 = (ballX + startX)**2 + (ballY - startY)**2  # 공과 위쪽 벽 사이의 거리를 계산
        dists.append(d2) # 계산된 거리를 리스트에 추가
        
    # 오른쪽 벽
    # 단, y좌표가 같고 목표의 x가 더 크면 안됨
    if not (ballY == startY and ballX > startX):
        d2 = (ballX - 2*x+startX)**2 + (ballY - startY)**2
        dists.append(d2)
    return min(dists) # 계산된 거리 중 가장 작은 값을 반환
    
def solution(m, n, startX, startY, balls):
    '''
    m,n: 벽의 가로세로 길이
    startX, startY: 시작점의 x와 y좌표
    '''
    answer = []
    for ballX, ballY in balls: # 주어진 목표점들의 좌표를 하나씩 가져와서 반복
        answer.append(solve(m, n, startX, startY, ballX, ballY)) # solve 함수를 호출하여 해당 목표지점까지의 거리를 계산하고 그 값을 answer 리스트에 추가
    return answer # 모든 목표점들에 대한 거리가 담긴 리스트 반환
