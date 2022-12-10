def double_round(x: float, u: float): # only for u < 10
    try:
        assert u < 10
        u_str = str(u).replace(".", "")
        n = -1
        for i in range(len(u_str)):
            if u_str[i] != '0':
                if int(u_str[i]) < 3:
                    n = i + 1
                else:
                    n = i
                break
        return round(x, n), round(u, n)
    except:
        return -1, -1


#test1
print("test1 passed" if double_round(2.0335000005, 0.00710985) == (2.034, 0.007) else "test1 failed")
#test2
print("test2 passed" if double_round(1.0299999999, 0.0471168) == (1.03, 0.05) else "test2 failed")
#test3
print("test3 passed" if double_round(500, 0.4898979) == (500.0, 0.5) else "test3 failed")
#test4
print("test4 passed" if double_round(21.5, 1.2288205) == (21.5, 1.2) else "test4 failed")
#test5
print("test5 passed" if double_round(23.39485430, 12.3332) == (-1, -1) else "test5 failed")