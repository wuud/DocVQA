def judge_number(str):
    flag = True
    for x in str:
        if x.isdigit() or x == '.' or x == ',' or x == '-':
            continue
        else:
            flag = False
            break
    return flag