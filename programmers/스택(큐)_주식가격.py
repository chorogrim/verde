# 초 단위로 기록된 주식가격이 담긴 배열 prices가 매개변수로 주어질 때,
# 가격이 떨어지지 않은 기간은 몇초인지를 return 하도록 solution 함수를 완성하세요.

def solution(prices): # solution 함수를 정의하고, 하나의 매개변수 prices를 받음
    answer = [] # 결과를 저장할 빈 리스트 answer를 초기화
    for i in range(len(prices)): # 입력 리스트 prices의 길이만큼 반복
        count = 0 # 현재 가격에서 유지된 기간을 세는 변수 count를 초기화
        for j in range(i+1,len(prices)): # 현재 가격 이후의 가격들을 순회
            if(prices[i]<= prices[j]): # 현재 가격이 이후의 가격보다 작거나 같으면 가격이 유지되는 것으로 간주
                count+=1 # count를 1증가
            else: # 현재 가격이 이후의 가격보다 크다면 가격이 하락한 것으로 판단하고, 더 이상 유지된 기간을 세지 않음
                count+=1 # 아래 break로 인해 더이상 순회하지 않음
                break # 내부 반복문을 종료
        answer.append(count) # 현재 가격에서 유지된 기간을 answer 리스트에 추가
    return answer # answer 리스트를 반환

print(solution([1, 2, 3, 2, 3]))
