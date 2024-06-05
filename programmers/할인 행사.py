def solution(want, number, discount):
    '''
    want: 원하는 아이템 리스트
    number: 각 아이템의 원하는 수량 리스트
    discount: 할인 아이템 리스트
    '''
    answer = 0 # 원하는 아이템들을 모두 포함하는 10일 연속 기간의 횟수를 저장
    dict_wishlist = {} # 원하는 아이템과 수량을 저장하는데 사용
    
    for i in range(len(want)): # want 리스트를 순회하면서 각 아이템과 그 수량을 dict_wishlist에 저장
        dict_wishlist[want[i]] = number[i] # 아이템 이름을 키로, 원하는 수량을 값으로 함
        
    for i in range(len(discount) - 9): # 리스트를 순회하면서 10일 연속 기간을 확인  
        dict_tmp = dict_wishlist.copy() # 현재 10일 기간 동안의 아이템 수량을 추적하는데 사용
        for j in range(i, i + 10): # i부터 i+10일까지 10일 동안의 아이템을 확인 
            if discount[j] in dict_tmp and dict_tmp[discount[j]] != 0: # discount[j] 아이템이 dict_tmp에 있고
                dict_tmp[discount[j]] -= 1 # 수량이 0이 아니면 그 아이템의 수량을 1 줄임
            else: # 그렇지 않으면
                break # 아이템들을 모두 포함하지 않으므로 종료
        if sum(dict_tmp.values()) == 0: # dict_tmp의 모든 값의 합이 0이면, 원하는 모든 아이템들이 포함된 것이므로
            answer += 1 # answer를 1 증가
            
    return answer # 원하는 아이템들을 모두 포함하는 10일 연속 기간의 횟수인 answer를 반환