# 백준 알고리즘 1991 문제
# 이진 트리를 입력받아 전위 순회, 중위 순회, 후위 순회한 결과를 출력하는 프로그램을 작성하시오.
# 전위 순회 -> a-b-d-c-e-f-g 
# 중위 순회 -> d-b-a-e-c-f-g 
# 후위 순회 -> d-b-e-g-f-c-a 


import sys

# 입력받을 n값을 선언
n = int(sys.stdin.readline())
# dict을 선언
tree = dict()

# 반복문을 통해 트리 생성
for i in range(n):
    # root, left, right를 
    root, left, right = map(str, sys.stdin.readline().split())
    # tree의 root를 left, right로 선언
    tree[root] = left, right

# 전위 순회 preorder = (루트)(왼쪽 자식)(오른쪽 자식)
def preorder(v):
    # 자식이 있다면
    if v != '.':
        # 루트 노드 출력
        print(v, end = '')
        # 재귀적으로 왼쪽 노드 탐색
        preorder(tree[v][0])
        # 재귀적으로 오른쪽 노드 탐색
        preorder(tree[v][1])

# 중위 순회 inorder = (왼쪽 자식)(루트)(오른쪽 자식)
def inorder(v):
    # 자식이 있다면
    if v != '.':
        # 재귀적으로 왼쪽 노드 탐색
        inorder(tree[v][0])
        # 루트 노드 출력 후 띄어쓰기
        print(v, end='')
        # 재귀적으로 오른쪽 노드 탐색
        inorder(tree[v][1])

# 후위 순회 postorder = (왼쪽 자식)(오른쪽 자식)(루트)
def postorder(v):
    # 자식이 있다면
    if v != '.':
        # 재귀적으로 왼쪽 노드 탐색
        postorder(tree[v][0])
        # 재귀적으로 오른쪽 노드 탐색
        postorder(tree[v][1])
        # 루트 노드 출력 후 띄어쓰기
        print(v, end='')
        
preorder('A')
print()
inorder('A')
print()
postorder('A')
