import random

def bubble(d:list):
    x = len(d)-1
    for i in range(x):
        for j in range(x-i):
            if d[j] > d[j+1]:
                d[j+1],d[j] = d[j],d[j+1]
    return d

size = 20
d = [random.randint(1, 100) for _ in range(size)]
print('ソート前：',*d)
print('ソート後：',*bubble(d))