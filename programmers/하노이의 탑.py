def solution(n):
    answer = [] # 원판을 옮긴 경로를 저장할 빈 리스트 
    
    def move(n, start, des, temp):
        a = []
        if(n == 1): # 만약 옮겨야 할 원판이 1개라면
            a.append(start) # 출발 기둥 번호를 리스트 a에 추가
            a.append(des) # 목적지 기둥 번호를 리스트 a에 추가
            answer.append(a) # 리스트 a를 answer에 추가
            return # 함수를 종료
        move(n-1, start, temp, des) # 가장 큰 원판을 제외하고 나머지 원판들을 start에서 temp로 옮김
        a.append(start) # 가장 큰 원판을 start에서 des로 옮긴 후 출발 기둥 번호를 리스트 a에 추가
        a.append(des) # 가장 큰 원판을 start에서 des로 옮긴 후 목적지 기둥 번호를 리스트 a에 추가
        answer.append(a) # 원판을 옮긴 경로를 리스트 a로 표현하여 answer 리스트에 추가
        move(n-1, temp, des, start) # temp에 옮겨둔 원판들은 목적지 기둥 des로 옮김
    move(n, 1, 3, 2) # 처음에는 모든 원판이 1번 기둥에 있고, 목적지는 3번 기둥이며, 보조 기둥은 2번
    return answer # 원판을 옮긴 경로를 담고 있는 answer 리스트를 반환
