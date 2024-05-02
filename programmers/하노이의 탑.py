# 1번 기둥에 있는 원판의 개수 n이 매개변수로 주어질 때,
# n개의 원판을 3번 원판으로 최소로 옮기는 방법을 return하는 solution를 완성해주세요.

def solution(n):
    answer = []
    
    def move(n, start, des, temp):
        a = []
        if(n == 1):
            a.append(start)
            a.append(des)
            answer.append(a)
            return
        move(n-1, start, temp, des)
        a.append(start)
        a.append(des)
        answer.append(a)
        move(n-1, temp, des, start)
    move(n, 1, 3, 2)
    return answer