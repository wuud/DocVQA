import json
import os
import utils
import sys
import random
sys.path.append('/mnt/workspace/DocVQA/src')


def getTrainDatasMid(col_name1, col_name2, name):
    res = {}
    res['data'] = list()
    ctx = utils.Context()
    for key in ctx.modelsMap_.keys():
        unit = ctx.modelsMap_[key]
        # if unit != None:
        #     num1, num2 = unit.num1, unit.num2
        # else:
        num1, num2 = random.randint(
            1000000000, 10000000000), random.randint(1000000000, 10000000000)

        item1 = {}
        item1['instruction'] = '{5}公司{0}的{2}为{3}元，{1}的{2}为{4}元，问{5}公司{0}的{2}是多少？'.format(
            col_name1, col_name2, key, num1, num2, name)
        item1['input'] = ""
        item1['output'] = "{3}公司{0}的{1}是{2}元。".format(
            col_name1, key, num1, name)
        res['data'].append(item1)

        item2 = {}
        item2['instruction'] = '{5}公司{0}的{2}为{3}元，{1}的{2}为{4}元，问{5}公司{1}的{2}是多少？'.format(
            col_name1, col_name2, key, num1, num2, name)
        item2['input'] = ""
        item2['output'] = "{3}公司{0}的{1}是{2}元。".format(
            col_name2, key, num2, name)
        res['data'].append(item2)
    return res


def getTrainDatasAll(col_name1, col_name2, name):
    res = {}
    res['data'] = list()
    ctx = utils.Context(dict())
    for key in ctx.modelsMap_.keys():
        unit = ctx.modelsMap_[key]
        num1, num2 = random.randint(
            1000000000, 10000000000), random.randint(1000000000, 10000000000)

        item1 = {}
        item1['instruction'] = '{5}公司{2}的{0}为{3}元，{2}的{1}为{4}元，问{5}公司{2}的{0}是多少？'.format(
            col_name1, col_name2, key, num1, num2, name)
        item1['input'] = ""
        item1['output'] = "{3}公司{0}的{1}是{2}元。".format(
            key, col_name1, num1, name)
        res['data'].append(item1)

        item2 = {}
        item2['instruction'] = '{5}公司{2}的{0}为{3}元，{2}的{1}为{4}元，问{5}公司{2}的{1}是多少？'.format(
            col_name1, col_name2, key, num1, num2, name)
        item2['input'] = ""
        item2['output'] = "{3}公司{0}的{1}是{2}元。".format(
            key, col_name2, num2, name)
        res['data'].append(item2)
    return res


def getTrainDatasIncremental(col_name1, col_name2, name):
    res = {}
    res['data'] = list()
    ctx = utils.Context('')
    for key in ctx.modelsMap_.keys():
        unit = ctx.modelsMap_[key]
        num1, num2 = float(random.randint(
            1000000000, 10000000000)), float(random.randint(1000000000, 10000000000))

        item2 = {}
        item2['instruction'] = '已知{5}公司{2}的{0}为{3}，{1}为{4}，问{5}公司{2}的增长率多少？'.format(
            col_name1, col_name2, key, num1, num2, name)
        item2['input'] = ''
        # item2['output'] = '''{6}公司{2}的增长率可以通过以下公式计算：增长率 = ({0} - {1}) * 100 / {1}。根据给定数据，我们可以进行如下计算：增长率 = ({3} - {4}) * 100 / {4} = {5}%。因此，{6}公司{2}的增长率为{5}%'''.format(
        #     col_name1, col_name2, key, num1, num2, round((num1 - num2) * 100 / num2, 2), name)
        item2['output'] = '''增长率 = ({3} - {4}) * 100 / {4}'''.format(
            col_name1, col_name2, key, num1, num2, round((num1 - num2) * 100 / num2, 2), name)
        res['data'].append(item2)
    return res

def getTrainDatasIncrementalMid(col_name1, col_name2, name):
    res = {}
    res['data'] = list()
    ctx = utils.Context()
    for key in ctx.modelsMap_.keys():
        unit = ctx.modelsMap_[key]
        num1, num2 = float(random.randint(
            1000000000, 10000000000)), float(random.randint(1000000000, 10000000000))

        item2 = {}
        item2['instruction'] = '已知{5}公司{0}的{2}为{3}，{1}的{2}为{4}，问{5}公司上半年{2}的增长率多少？'.format(
            col_name1, col_name2, key, num1, num2, name)
        item2['input'] = ''
        item2['output'] = '''{6}公司上半年{2}的增长率可以通过以下公式计算：增长率 = ({0}的{2} - {1}的{2}) * 100 / {1}的{2}。根据给定数据，我们可以进行如下计算：增长率 = ({3} - {4}) * 100 / {4} = {5}%。因此，{6}公司{2}的增长率为{5}%'''.format(
            col_name1, col_name2, key, num1, num2, round((num1 - num2) * 100 / num2, 2), name)
        res['data'].append(item2)
    return res


if __name__ == '__main__':

    dic = {}
    dic['data'] = list()
    
    for name in ('廊坊千翼千行','都城伟业'):
        temp = []
        # temp.append(getTrainDatasMid('2022年6月30日', '2021年12月31日', name)) 
        temp.append(getTrainDatasAll('期末余额', '期初余额', name))
        temp.append(getTrainDatasAll('本期金额', '上期金额', name))
        temp.append(getTrainDatasIncremental('本期金额', '上期金额', name))
        temp.append(getTrainDatasIncremental('期末余额', '期初余额', name))
        # temp.append(getTrainDatasIncrementalMid('2022年6月30日', '2021年12月31日', name))
        for d in temp:
            dic['data'].extend(d['data'])

    with open('train_data.json', 'w') as f:
        json.dump(dic['data'], f, ensure_ascii=False, indent=4)
