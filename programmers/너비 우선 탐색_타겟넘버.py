# 사용할 수 잇는 숫자가 담긴 배열 numbers, 타겟 넘버 target이 매개변수로 주어질 때
# 숫자를 적절히 더하고 빼서 타겟 넘버를 만드는 방법의 수를 return 하도록 solution 함수를 작성해주세요.

def solution(numbers, target):
    answer = 0
    ansList = [0]
    
    for num in numbers:
        tmpList = []
        for a in ansList:
            tmpList.append(a+num)
            tmpList.append(a-num)
        ansList = tmpList
    for a in ansList:
        if a == target:
            answer += 1
    return answer
