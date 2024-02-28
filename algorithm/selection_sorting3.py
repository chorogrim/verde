# 백준 알고리즘 25305번 문제
# 2022 연세대학교 미래캠퍼스 슬기로운 코딩생활에 N명의 학생들이 응시했다.
# 이들 중 점수가 가장 높은 k명은 상을 받음. 이 때, 상을 받는 커트라인이 몇 점인지 구하라.
# 커트라인이란 상을 받는 사람들 중 점수가 가장 가장 낮은 사람의 점수를 말한다.


N, k = map(int,input().split()) # 입력을 받아서 공백을 기준으로 분리된 값들을 정수형으로 변환한 후,
                                # N과 K라는 변수에 각각 할당

scores = list(map(int, input().split())) # 여러 개의 숫자를 입력받아 리스트로 저장
scores.sort(reverse=True) # 내림차순으로 정렬

print(scores[k-1]) # 그 중에서 k번째로 큰 값을 출력

