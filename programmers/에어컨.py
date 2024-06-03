def solution(temperature, t1, t2, a, b, onboard):
    '''
    temperature: 현재 온도
    t1: 최소 희망 온도
    t2: 최대 희망 온도
    a: 에어컨을 켜서 온도를 1도 변경하는데 드는 전력
    b: 에어컨을 켜서 온도를 유지하는데 드는 전력
    onboard: 각 분마다 사람이 탑승해 있는지를 나타내는 리스트

    '''
    k = 1000 * 100
    t1 += 10
    t2 += 10
    temperature += 10
    
    # DP[i][j] : i분에 j 온도를 만들 수 있는 가장 적은 전력
    DP = [[k] * 51 for _ in range(len(onboard))] # DP[i][j]는 i분에 j온도를 만들 수 있는 최소 전력을 나타냄
    DP[0][temperature] = 0
    
    flag = 1 # 에어컨이 작동할 때 온도가 증가하는지 감소하는지를 나타냄
    if temperature > t2 :
        flag = -1
 
    for i in range(1, len(onboard)): # 1분까지의 시간과 각 온도에 대해 반복
        for j in range(51):
            arr = [k]
            if (onboard[i] == 1 and t1 <= j <= t2) or onboard[i] == 0:
                # 1. 에어컨을 키지 않고 실외온도와 달라서 실내온도가 -flag 되는 경우
                if 0 <= j+flag <= 50 :
                    arr.append(DP[i-1][j+flag])
                # 2. 에어컨을 키지 않고 현재온도 j 가 실외온도랑 같아서 변하지 않는 경우
                if j == temperature:
                    arr.append(DP[i-1][j])
                # 3. 에어컨을 키고 현재온도가 변하는 경우
                if 0 <= j-flag <= 50:
                    arr.append(DP[i-1][j-flag] + a)
                # 4. 에어컨을 키고 현재온도가 희망온도라서 온도가 변하지 않는 경우
                if t1 <= j <= t2:
                    arr.append(DP[i-1][j] + b)

                DP[i][j] = min(arr)
            
    answer = min(DP[len(onboard)-1]) # 마지막 시간에 모든 온도에서의 최소 전력 소비를 찾고
    return answer # 그 중 최소 값을 반환
