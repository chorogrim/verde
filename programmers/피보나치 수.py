def solution(n):
    arr = [] # 빈 리스트 arr를 생성. 피보나치 수열의 각 항을 저장
    arr.append(0) # 피보나치 수열의 첫 번째 항은 0
    arr.append(1) # 피보나치 수열의 두 번째 항은 1
    arr.append(1) # 피보나치 수열의 세 번째 항은 1
    
    for i in range(1, n-1): # 피보나치 수열의 성질을 이용하여 누적값을 계산하기 위해 반복문을 실행
        arr.append(arr[i]+ arr[i+1]) # arr에 현재 항의 이전 두 항을 더한 값을 추가
    return arr[n] % 1234567 # 계산된 피보나치 수열의 n번째 항을 반환
