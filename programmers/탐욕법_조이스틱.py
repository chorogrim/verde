# 만들고자 하는 이름 name이 매개변수로 주어질 때, 
# 이름에 대해 조이스틱 조작 횟수의 최솟값을 return 하도록 solution 함수를 만드세요.

def solution(name):
    count = 0 # 문자열을 완성하기 위해 상하 방향키로 조작하는 횟수를 누적
    size = len(name) # 입력된 문자열의 길이를 나타내는 변수
    min_move = size - 1 # 좌우 방향키로 이동할 때의 최소 이동 횟수를 초기화

    for idx, char in enumerate(name): # 문자열 name의 각 문자에 대해 반복
        count += min(ord(char) - ord('A'), ord('Z') - ord(char) + 1) # 현재 문자를 완성하기 위해 상하 방향키로 조작하는 횟수를 계산
        
        next_idx = idx + 1 # 다음 인덱스를 설정
        while next_idx < size and name[next_idx] == 'A': # 연속된 A를 만나면 다음 문자로 이동
            next_idx += 1 

        min_move = min([min_move, 2 * idx + size - next_idx, idx + 2 * (size - next_idx)]) # 좌우 방향키로 이동할 때의 최소 이동 횟수를 계산

    count += min_move # 상하 방향키 조작 횟수와 좌우 이동 횟수를 합하여 최종 결과를 반환
    return count # 함수의 결과를 반환
