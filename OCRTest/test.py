def str_number(str):
    num = 0.0
    pre_str = str[0:-3]
    for x in pre_str:
        if x != '.' and x != ',':
            num = num * 10 + int(x)
    num = num + float(str[-2:])/100
    # print(num)
    return num
    # print(str[-2:])

# str_number("194,320,423,423.56")