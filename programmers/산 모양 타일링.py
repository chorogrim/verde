def solution(n, tops):
    '''
    n: 삼각형의 개수
    tops: 각 삼각형의 꼭짓점 여부를 나타내는 리스트
    '''
    MOD = 10007 # 나머지 연산을 위한 상수 MOD를 10007로 설정

    cache1 = [0] * (n + 1)  # cache1[i]: 밑변의 i번째 삼각형이 왼쪽 방향 마름모 모양
    cache2 = [0] * (n + 1)  # cache2[i]: cache1이 아닌 경우
    cache1[0] = 0 
    cache2[0] = 1 

    for i in range(1, n + 1):
        cache1[i] = (cache1[i - 1] + cache2[i - 1]) % MOD # i번째 삼각형이 왼쪽 방향 마름모 모양일 때의 경우의 수를 계산

        if tops[i - 1]: # 삼각형의 꼭짓점 여부를 확인
            cache2[i] = (2 * cache1[i - 1] + 3 * cache2[i - 1]) % MOD # 꼭짓점이 있는 경우 
        else:
            cache2[i] = (cache1[i - 1] + 2 * cache2[i - 1]) % MOD # 꼭짓점이 없는 경우

    return (cache1[n] + cache2[n]) % MOD # n번째 삼각형이 왼쪽 방향 마름모 모양인 경우의 수와 그렇지 않은 경우의 수를 더한 후 MOD로 나눈 나머지를 반환
