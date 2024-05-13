def solution(edges):
    answer = [0, 0, 0, 0] # 생성 노드, 도넛 그래프, 막대 그래프, 8자 그래프
    max_val = max(map(max, edges)) + 1  # 리스트에서 최대 값보다 1 큰 값을 max_val에 저장
    in_cnt, out_cnt = [0] * max_val, [0] * max_val # in_cnt와 out_cnt라는 두 개의 리스트를 생성
        
    # in, out 간선 저장
    for now_out, now_in in edges: # 해당 엣지의 출발 노드, 도착 노드
        out_cnt[now_out] += 1 # 현재 엣지의 출발 노드와 도착 노드에 대해 나가는 간선과 
        in_cnt[now_in] += 1   # 들어오는 간선의 수를 증가
        
    for now_node in range(1, max_val): #  1부터 max_val까지의 범위에서 각 노드를 반복
        if in_cnt[now_node] == 0 and out_cnt[now_node] >= 2: # 생성 노드
            answer[0] = now_node 
        elif in_cnt[now_node] >= 1 and out_cnt[now_node] == 0: # 막대 그래프
            answer[2] += 1
        elif in_cnt[now_node] >= 2 and out_cnt[now_node] == 2: # 8자 그래프 
            answer[3] += 1
    answer[1] = out_cnt[answer[0]] - sum(answer[2:])    # 도넛 그래프
    
    return answer