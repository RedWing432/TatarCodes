n = int(input())
a = list(map(int, input().split()))
m = int(input())
p = []

for i in range(m):
    t, k = map(int, input().split())
    o = t - 1
    g = 0
    while o < k:
        if a[o] == 0:
            g = g + 1
        o = o + 1
    p.append(g)
print(*p)
        
