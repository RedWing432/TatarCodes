import sys
stdout = sys.stdout
sys.stdin = 2
sys.stdout = open('user_output_1.txt', 'w')
print('салам', input())