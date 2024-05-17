def solution(n, tops):
    MOD = 10007

    cache1 = [0] * (n + 1)  # cache1[i]: 밑변의 i번째 삼각형이 왼쪽 방향 마름모 모양
    cache2 = [0] * (n + 1)  # cache2[i]: cache1이 아닌 경우
    cache1[0] = 0
    cache2[0] = 1

    for i in range(1, n + 1):
        cache1[i] = (cache1[i - 1] + cache2[i - 1]) % MOD

        if tops[i - 1]:
            cache2[i] = (2 * cache1[i - 1] + 3 * cache2[i - 1]) % MOD
        else:
            cache2[i] = (cache1[i - 1] + 2 * cache2[i - 1]) % MOD

    return (cache1[n] + cache2[n]) % MOD