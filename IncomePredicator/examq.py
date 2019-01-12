def what(n):
    print(n)
    if n == 0:
        print(n)
        return 0
    else:
        print(n)
        return n + what(n-1)


what(-3)