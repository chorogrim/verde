def solution(cap, n, deliveries, pickups):
    d, p, answer = 0, 0, 0
    for i in range(n-1, -1, -1): # 마지막 집부터 확인
        d += deliveries[i] # 배달해야 할 양 확인
        p += pickups[i] # 수거해야 할 양 확인
        
        while d > 0 or p > 0: # 만약 둘 중 하나가 양수라면? 무조건 물류 창고를 돌려야한다
            d -= cap # 물류 창고를 돌려야하니까 그만큼 배달 해준거니 빼주고
            p -= cap # 수거도 마찬가지로 빼준다
            answer += (i + 1)* 2 # 거리는 i+1에 왕복으로 갔다오니 *2
    return answer