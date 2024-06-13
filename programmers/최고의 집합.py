def solution(n, s):
    answer = []

    if s<n: # s가 n보다 작다면
        return [-1] # s를 n개의 숫자로 나눌 수 없으므로 [-1]을 반환
    
    num = s//n # s를 n으로 나눈 몫을 sum에 저장
    rest = s%n # s 를 n으로 나눈 나머지를 rest에 저장
    
    for idx in range(n): # n번 반복하며
        answer.append(num) #  num을 answer 리스트에 추가

    if rest != 0: # rest가 0이 아니라면
        for a in range(len(answer)): # 반복하면서
            answer[a] += 1 # answer 리스트의 각 요소에 1을 더해줌
            rest -= 1 # rest 값을 1씩 줄임
            if rest == 0: # rest가 0이라면
                break # 반복문 종료
    answer.sort() # 리스트를 오름차순으로 정렬
    return answer # answer 리스트 반환