def solution(n, k, cmd):
    # key: 행 번호, value: [이전행, 다음행]
    table = {i:[i-1, i+1] for i in range(n)} # 표
    table[0] = [None, 1]
    table[n-1] = [n-2, None]

    exist = ['O'] * n  # 삭제된 행 표시용 리스트
    deleted = [] # 삭제된 행을 저장할 리스트

    # 명령어 하나씩 수행
    for command in cmd:
        oper = ''
        move = 0
        # 명령어 길이에 따라 parsing
        if len(command) == 1:
            oper = command
        else:
            oper, move = command.split()
            move = int(move)

        if oper == 'U':
            # 현재 선택된 행에서 move칸 위에 있는 행 선택
            for _ in range(move):
                k = table[k][0]
        elif oper == 'D':
            # 현재 선택된 행에서 move칸 아래에 있는 행 선택
            for _ in range(move):
                k = table[k][1]
        elif oper == 'C':
            # 현재 선택된 행 삭제 후 바로 아래 행 선택
            # -> k는 그대로 있으면 됨
            # (현재 선택된 행 k, k번째 컬럼의 앞, 뒤 행 번호) 튜플 저장
            prev, next = table[k]
            deleted.append((k, prev, next))
            # 삭제된 행 표시
            exist[k] = 'X'
            # 커서 변경
            # 삭제된 행이 가장 마지막 행이라면 바로 윗 행 선택
            if next == None:
                k = table[k][0]
            else:
                k = table[k][1]
            # 삭제된 행이 가장 윗 행이라면 다음 행의 이전 행 번호 0
            if prev == None:
                table[next][0] = None
            # 마지막 행이라면 이전 행의 다음 행 번호 0
            elif next == None:
                table[prev][1] = None
            # 중간에 있으면 next, prev 갱신
            else:
                table[prev][1] = next
                table[next][0] = prev
        elif oper == 'Z':
            # 가장 최근에 삭제된 행 원래대로 복구
            # 현재 선택된 행은 바뀌지 않음
            # 삭제 리스트 맨 뒤에서 꺼내옴
            idx, prev, next = deleted.pop()
            # 테이블 삽입 
            if prev == None:
                table[next][0] = idx
            elif next == None:
                table[prev][1] = idx
            else:
                table[prev][1] = idx
                table[next][0] = idx
            # 되돌린 행 표시
            exist[idx] = 'O'

    answer = "".join(exist)

    return answer