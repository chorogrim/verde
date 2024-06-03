def solution(cap, n, deliveries, pickups):
    '''
    cap: 한 번에 배달하거나 수거할 수 있는 최대 용량
    n: 배달 및 수거해야 할 집의 수
    deliveries: 각 집마다 배달해야 할 물건의 수를 담은 리스트
    pickups: 각 집마다 수거해야 할 물건의 수를 담은 리스트
    '''

    deliveries = deliveries[::-1] # deliveries 리스트를 역순으로 뒤집기 (끝에서 시작)
    pickups = pickups[::-1]
    answer = 0
    
    d = 0 # 배달할 물건을 추적하기 위한 변수를 0으로 초기화
    p = 0 # 수거해야 할 물건을 추적하기 위한 변수를 0으로 초기화
    
    for i in range(n):
        d += deliveries[i] # 현재 집의 배달할 물건
        p += pickups[i] # 수거할 물건
        
        while d > 0 or p > 0:
            d -= cap # 배달할 물건에서 한 번에 운반할 수 있는 최대 용량을 뺌
            p -= cap # 수거할 물건에서 한 번에 운반할 수 있는 최대 용량을 뺌
            answer += (n-i)*2 # (n-1)는 현재 집에서 끝까지의 거리, *2는 왕복 거리

    return answer
