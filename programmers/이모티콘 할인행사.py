from itertools import product

def solution(users, emoticons):
    '''
    users: 각 사용자의 할인율과 지출 한도를 나타내는 리스트
    emoticons: 이모티콘의 원래 가격을 나타내는 리스트
    '''
    answer = [-1, -1]  # 최대 판매 수와 최소 비용 초기화

    # 할인율의 모든 조합을 생성
    for discounts in product([10, 20, 30, 40], repeat=len(emoticons)): # 할인율은 10%, 20%, 30%, 40%
        sale_num = 0  # 판매 수
        cost_num = 0  # 비용

        # 각 사용자에 대해 계산
        for user in users:
            # 각 사용자의 할인율과 이모티콘 가격을 기반으로 사용자가 구매할 수 있는 이모티콘의 총 비용 tmp를 계산
            tmp = sum([emoticon * (1 - discount / 100) for discount, emoticon in zip(discounts, emoticons) if user[0] <= discount])
            if tmp >= user[1]: # 사용자의 총 비용이 지출 한도를 넘는 경우, 판매 수를 1 증가
                sale_num += 1
            else:
                cost_num += tmp # 사용자의 총 비용이 지출 한도를 넘지 않는 경우, 총 비용 tmp를 더함

        # 최대 판매 수와 최소 비용 갱신
        if sale_num > answer[0] or (sale_num == answer[0] and cost_num > answer[1]):
            answer = [sale_num, cost_num]

    return answer # 최대 판매 수와 최소 비용을 저장한 answer 리스트를 반환
