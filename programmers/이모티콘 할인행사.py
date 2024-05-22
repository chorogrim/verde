from itertools import product

def solution(users, emoticons):
    answer = [-1, -1]  # 최대 판매 수와 최소 비용 초기화

    # 할인율 조합 생성
    for discounts in product([10, 20, 30, 40], repeat=len(emoticons)):
        sale_num = 0  # 판매 수
        cost_num = 0  # 비용

        # 각 사용자에 대해 계산
        for user in users:
            tmp = sum([emoticon * (1 - discount / 100) for discount, emoticon in zip(discounts, emoticons) if user[0] <= discount])
            if tmp >= user[1]:
                sale_num += 1
            else:
                cost_num += tmp

        # 최대 판매 수와 최소 비용 갱신
        if sale_num > answer[0] or (sale_num == answer[0] and cost_num > answer[1]):
            answer = [sale_num, cost_num]

    return answer