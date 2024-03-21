# フィボナッチ数列の表示

def fib(end):
    fibo = [1, 1]
    while len(fibo) < end:
        fibo.append(fibo[-1]+fibo[-2])
    return fibo

print(*fib(20))