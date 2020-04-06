"""
    斐波那契数列

"""
import  time

def fib(n):
    """
        简单递归
        时间复杂度 O(2^n)
    """
    if n <= 2:
        return 1
    return fib(n-1)+fib(n-2)


def _fib(n, array):
    if n <= 2:
        return 1
    if array[n] == 0:
        array[n] = _fib(n - 1, array) + _fib(n - 2, array)
    return array[n]


def fib2(n):
    """
        避免重复计算-使用备忘录
        时间复杂度 O(n)
    """
    array = [0 for i in range(n+1)]
    array[1] = 1
    return _fib(n, array)

def fib3(n):
    """
        去除递归
        自底向上
    """
    array = [0 for i in range(n+1)]
    array[1] = 1
    for i in range(2, n+1):
        array[i] = array[i-1] + array[i-2]
    return array[n]

def fib4(n):
    """
        滚动数组
    """
    array = [0, 0]
    array[1] = 1
    for i in range(2, n+1):
        array[i % 2] = array[(i-1) % 2] + array[(i-2)%2]
    return array[n%2]


def fib5(n):
    """
        使用位运算
    """
    array = [0, 0]
    array[1] = 1
    for i in range(2, n+1):
        array[i & 1] = array[(i-1) & 1] + array[(i-2)& 1]
    return array[n & 1]

def fib6(n):
    """
        不使用数组
    """
    first = 0
    second = 1
    for i in range(2, n+1):
        second = first + second
        first = second - first
    return second

def fib7(n):
    """ 公式法
        pow等时间复杂度低至log(n)
    """
    pass

def fib_test(func, num):
    start = time.process_time()
    res = func(num)
    elapsed = (time.process_time() - start)
    print(res)
    print("Time used:",elapsed)


# fib_test(fib, 40)
# fib_test(fib2, 1000)
fib_test(fib3, 1000)
fib_test(fib4, 1000)
fib_test(fib5, 1000)
fib_test(fib6, 1000)
