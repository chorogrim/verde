# 마라톤에 참여한 선수들의 이름이 담긴 배열 participant와
# 완주한 선수들의 이름이 담긴 배열 completion이 주어질 때,
# 완주하지 못한 선수의 이름을 return 하도록 solution 함수를 작성해주세요.


def solution(participant, completion):
    answer = ''
    p_dict = {}
    
    for p in participant:
        if p not in p_dict:
            p_dict[p] = 1
        else:
            p_dict[p] += 1
            
    for c in completion:
        p_dict[c] -= 1
        
    for pd in p_dict:
        if p_dict[pd] == 1:
            answer = pd
    return answer
