import heapq

def solution(n, k, enemy):
    '''
    n: 초기 체력
    k: 회피할 수 있는 횟수
    enemy: 적의 리스트
    '''
    heap = []
    result = 0 # 이긴 적의 수를 세기 위해 초기화
    cnt = 0 # 누적된 적의 공격력 합을 추적하기 위해 초기화
    
    for e in enemy: # enemy 리스트를 순회하면서 공격력을 e로 가져옴
        heapq.heappush(heap, -e) # 적의 공격력을 최대 힙으로 만들기 위해 음수로 변환하여 heap에 추가
        cnt += e # cnt에 현재 적의 공격력을 더함
        if cnt > n: # 누적된 적의 공격력이 초기 체력보다 크다면 이길 수 없음을 의미
            if not k: # k이가 0이면 더 이상 회피할 수 없으므로
                return result # 지금까지 이긴 적의 수를 반환
            cnt += heapq.heappop(heap) # k가 0이ㅐ 아니면 회피 기회를 사용
            k-=1
        result += 1 # 적과 싸우는데 성공했으므로 result를 1 증가
    return result # 모든 적과의 싸움이 끝난 후, 이긴 적의 수를 반환