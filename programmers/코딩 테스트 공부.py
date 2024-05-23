def solution(alp, cop, problems): # apl: 알고리즘 능력, cop: 코딩 능력, problems: 문제 목록
    max_alp_req, max_cop_req = [0, 0]  # 0으로 초기화
    
    # 각 문제에서 요구하는 최대 알고리즘 능력과 최대 코딩 능력을 저장
    for problem in problems:
        max_alp_req = max(max_alp_req, problem[0])
        max_cop_req = max(max_cop_req, problem[1])
    
    # 모든 문제의 요구사항 중 최대값을 저장
    dp = [[float('inf')] * (max_cop_req+1) for _ in range(max_alp_req+1)]
    
    alp = min(alp, max_alp_req)  # 초기에는 모든 값을 무한대로 설정
    cop = min(cop, max_cop_req)
    
    dp[alp][cop] = 0  # dp[i][j]는 알고리즘 능력 i와 코딩 능력 j를 얻기 위한 최소 비용 저장
    
    for i in range(alp, max_alp_req+1): # alp부터 max_alp_req까지, cop부터 max_cop_req까지 반복
        for j in range(cop, max_cop_req+1):
            # 알고리즘 공부를 하여 i+1로 이동하는 경우 비용 계산
            if i < max_alp_req:
                dp[i+1][j] = min(dp[i+1][j], dp[i][j] + 1)
            # 코딩 공부를 하여 j+1로 이동하는 경우 비용 계산
            if j < max_cop_req:
                dp[i][j+1] = min(dp[i][j+1], dp[i][j] + 1)
            # 각 문제를 순회하면서 현재 능력 i와 j가 문제의 요구 능력 alp_req와 cop_req를 충족하는지 확인
            for alp_req, cop_req, alp_rwd, cop_rwd, cost in problems:
                if i >= alp_req and j >= cop_req:
                    new_alp = min(i+alp_rwd, max_alp_req) 
                    new_cop = min(j+cop_rwd, max_cop_req)
                    dp[new_alp][new_cop] = min(dp[new_alp][new_cop], dp[i][j] + cost)
    # 최대 요구 능력에 도달했을 때의 최소 비용 반환          
    return dp[max_alp_req][max_cop_req]