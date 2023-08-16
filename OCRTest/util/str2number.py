def str_number(str):
    if str.count('.') == 0:
        num = 0
        flag = True
        for x in str:
            if x == '-':
                flag = False
                continue
            if x != ',':
                num = num * 10 + int(x)
        if not flag:
            num = -1 * num
        return num
    num = 0.0
    pre_str = str[0:-3]
    # 判断是否为正数
    flag = True
    for x in pre_str:
        if x == '-':
            flag = False
            continue
        if x != '.' and x != ',':
            num = num * 10 + int(x)
    num = num + float(str[-2:]) / 100
    # print(num)
    if not flag:
        num = -1 * num
    return num