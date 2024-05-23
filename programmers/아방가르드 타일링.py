def solution(n):
    dp = [1,1,3,10] + [0]*(n-3) # dp 리스트를 초기화. 각 항의 값을 저장 
    sp_c2, sp_c3 = 2, 5 # sp_c2와 sp_c3를 초기화
    sp_cases = [12, 2, 4] # 특정 조건을 만족하는 경우의 값을 저장
    
    if n <= 3 : return dp[n] # 만약 n이 3 이하라면, 초기화된 dp 리스트의 값을 바로 반환
    
    for idx in range(4,n+1): # idx를 4부터 n까지 반복
        sp_c = idx%3 # idx를 3으로 나눈 나머지
        total = sp_cases[sp_c] # total을 sp_cases 리스트의 sp_c 인덱스 값으로 초기화
        
        total += dp[idx-1] + sp_c2*dp[idx-2] + sp_c3*dp[idx-3] # dp[idx-1]: 바로 이전 항의 값, sp_c2 * dp[idx-2]: 두 번째 이전 항의 값에 sp_c2를 곱한 값,  sp_c3* dp[idx-3]: 세 번째 이전 항의 값에 sp_c3를 곱한 값
        dp[idx] = total # dp 리스트의 idx번째 값을 total로 설정
        
        sp_cases[sp_c] += dp[idx-1]*2 + dp[idx-2]*2 + dp[idx-3]*4 # dp[idx-1]*2: 바로 이전 항의 값에 2를 곱한 값,  dp[idx-2]*2: 두 번째 이전 항의 값에 2를 곱한 값, dp[idx-3]*4: 세 번째 이전 항의 값에 4를 곱한 값
        
    answer = dp[n]%1000000007 # dp[n] 값을 1000000007로 나눈 나머지를 반환
    
    return answer
