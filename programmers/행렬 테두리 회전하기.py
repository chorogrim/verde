def solution(rows, columns, queries):
    '''
    rows: 행의 수
    columns: 열의 수
    queries: 회전할 영역을 정의하는 쿼리 리스트
    '''
    answer = [] # 최종적으로 반환할 결과를 저장할 빈 리스트
    arr = [] # 행렬을 저장할 빈 리스트
    cnt = 1 # 시작 숫자를 나타내는 변수 cnt를 1로 초기화
    
    for _ in range(rows):# 주어진 rows 만큼 반복
        arr.append([cnt + x for x in range(columns)]) # 각 행마다 columns 개수만큼 숫자를 생성하여 행렬에 추가
        cnt += columns # 다음 행의 시작 숫자를 업데이트

    for q in queries: # 각 쿼리에 대해 반복
        x1, y1, x2, y2 = q # 쿼리에서 시작점과 끝점의 좌표를 가져옴
        x_len, y_len = x2 - x1, y2 - y1 # x와 y의 길이를 구함
        num_list = [] # 현재 쿼리에서 회전된 숫자들을 저장할 빈 리스트 
        s_x, s_y = x1 - 1, y1 - 1 # 행렬 상에서의 시작점 좌표를 설정
        tmp = arr[s_x][s_y] # 시작점의 값을 tmp에 저장

        # 우측 이동
        for i in range(1, y_len + 1):
            tmp = arr[s_x][s_y + i]
            num_list.append(tmp) 
        s_y += y_len # y좌표를 오른쪽 끝으로 업데이트

        # 아래쪽 이동
        for i in range(1, x_len + 1):
            tmp = arr[s_x + i][s_y]
            num_list.append(tmp)
        s_x += x_len # x좌표를 아래쪽 끝으로 업데이트

        # 좌측 이동
        for i in range(1, y_len + 1):
            tmp = arr[s_x][s_y - i]
            num_list.append(tmp)
        s_y -= y_len # y 좌표를 왼쪽 끝으로 업데이트

        # 위쪽 이동
        for i in range(1, x_len + 1):
            tmp = arr[s_x - i][s_y]
            num_list.append(tmp)
        s_x -= x_len # x좌표를 위쪽 끝으로 업데이트

        answer.append(min(num_list)) # num_list에서 최솟값을 answer 리스트에 추가

        cnt = -1
        # 우측 이동
        for i in range(1, y_len + 1):
            arr[s_x][s_y + i] = num_list[cnt]
            cnt += 1
        s_y += y_len # y 좌표를 오른쪽 끝으로 업데이트

        # 아래쪽 이동
        for i in range(1, x_len + 1):
            arr[s_x + i][s_y] = num_list[cnt]
            cnt += 1
        s_x += x_len # y 좌표를 왼쪽 끝으로 업데이트

        # 좌측 이동
        for i in range(1, y_len + 1):
            arr[s_x][s_y - i] = num_list[cnt]
            cnt += 1
        s_y -= y_len # 위쪽 이동하며 값을 업데이트

        # 위쪽 이동
        for i in range(1, x_len + 1):
            arr[s_x - i][s_y] = num_list[cnt]
            cnt += 1
