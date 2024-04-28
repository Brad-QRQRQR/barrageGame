# glob = 3
# def func(x):
#     y = x + glob
#     def inner():
#         return y + 1
#     return inner, abs

# f1, f2 = func(1)
# print(f1())
# print(f1())


# def outer(a):
#     b = a
#     def inner():
#         c = 3
#         def inner_inner(b):
#             r = b+c
#             return b+c
#         return inner_inner
#     return inner
# foo = outer(10)
# bar = foo()
# bar(1) # 4

class A:
    def __init__(self):
        self.attack_timer = [0, 0, 0]
        self.k = 0

    @property
    def k(self):
        return self.__k

    @k.setter
    def k(self, new):
        self.__k = new
        print('b')

    @property
    def attack_timer(self):
        for i in range(len(self.__a)):
            if self.__a[i] >= 5:
                self.__a[i] = 5
        return self.__a

    @attack_timer.setter
    def attack_timer(self, value):
        self.__a = value
        for i in range(len(self.__a)):
            print('a')
            if self.__a[i] >= 5:
                self.__a[i] = 5

a = A()
for i in range(7):
    a.attack_timer[0] = i
    a.k = i
    print(a.k)