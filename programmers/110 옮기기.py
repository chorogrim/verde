def solution(s):
    answer = []
    for arr in s:
        stack, num110, i = [], 0, 0 # 110의 개수를 세는 변수 
        while i < len(arr):
            if arr[i] == '0': # 현재 문자 arr[i]가 0인지 확인
                if len(stack) >= 2 and stack[-2] == '1' and stack[-1] == '1': # stack의 길이가 2이상이고, 마지막 두 문자가 11인 경우를 확인
                    stack.pop() # stack에서 두번 pop해서 마지막 두 문자 제거
                    stack.pop()
                    num110 += 1 # 110의 개수를 하나 증가
                    i += 1 # 인덱스 i도 하나 증가
                else: # 만족하지 않으면
                    stack.append(arr[i]) # 현자 문자 arr[i]를 stack에 추가
                    i += 1 # 인덱스 i 하나 증가
            else:
                stack.append(arr[i]) # 0이 아니라면 stack에 arr[i] 추가
                i += 1 # 인덱스 i 하나 증가
                
        stack = ''.join(stack[::-1]) # stack의 문자를 역순으로 하여 하나의 문자열로 만듦
        idx = stack.find('0') # 역순으로 된 stack 문자열에서 0이 처음으로 나타나는 인덱스 찾기
        
        if idx != -1: # 0이 존재하면
            res = stack[:idx] + '011' * num110 + stack[idx:] # 0 앞부분과 011을 num110 횟수만큼 반복한 문자열, 0 뒷부분을 결합하여 문자열 res 만듦
        else: # 0이 존재하지 않으면
            res = stack + '011' * num110 # stack 문자열의 끝에 011을 num110 횟수만큼 반복한 문자열 붙임
        answer.append(''.join(res[::-1])) # res를 다시 만들어 역순으로 만들고 answer 리스트에 추가
        
    return answer # answer 리스트 반환