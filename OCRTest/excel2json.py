import re

import pandas as pd
import json
import os
import shutil
from OCRTest.util import judge_number
from OCRTest.util import str2number

term_dict = {
    "期初余额": "期末余额",
    "期末余额": "期初余额",
    "本期金额": "上期金额",
    "上期金额": "本期金额"
}


# 去掉表头中的杂质
def delete_head_blank(list):
    for index, value in enumerate(list):
        if pd.isna(value):
            list[index] = 'unknown'
            continue
        want = re.findall('[\u4e00-\u9fa5a-zA-Z1-9]+', value, re.S)
        want = "".join(want)
        list[index] = want
    return list


def json_inputs(open_path):
    """
    返回json字符串列表
    :param path: 需要转换excel文件的路径
    :return: 返回json列表
    # TODO 存在表格版面分析不准，导致表格上方一行加入表格使得表头识别错误的情况
    # TODO 将读取的第一行与实际表头对比，例如包含项目的是表头，包含余额的是表头这样
    # TODO 如果第一行真是表头，但内容有误，要根据正确部分修正
    # TODO 但是，可能回存在回归错误的问题，将在逐步调试
    """
    df = pd.read_excel(open_path)
    # 获取列名字
    col_names = df.columns.tolist()
    # 把列名中的空格去掉
    col_names = delete_head_blank(col_names)
    flag = True
    # 当前这一行不是表头
    if col_names[0] != '项目':
        flag = False
        col_names = df.iloc[0].to_list()
        col_names = delete_head_blank(col_names)
    print(col_names)
    # 将期初余额、期末余额按照对应关系修正表头
    for i in range(len(col_names)):
        if '期初' in col_names[i]:
            col_names[i] = '期初余额'
        if '期末' in col_names[i]:
            col_names[i] = '期末余额'
        if '本期' in col_names[i]:
            col_names[i] = '本期金额'
        if '上期' in col_names[i]:
            col_names[i] = '上期金额'
    for key, value in term_dict.items():
        if key in col_names and value not in col_names:
            for i in range(len(col_names)):
                if col_names[i] == key and (col_names[i] == '期初余额' or col_names[i] == '上期金额'):
                    col_names[i - 1] = value
                    break
                if col_names[i] == key and (col_names[i] == '期末余额' or col_names[i] == '本期金额'):
                    col_names[i + 1] = value
                    break

    # 修改列名字
    df.columns = col_names

    cols = [colName for colName in df.columns]
    print(cols)
    json_list = {}
    idx = 0
    if not flag:
        idx = idx + 1
    for row in df.itertuples():
        if idx >= 0:
            # print(row)
            idx = idx - 1
            continue
        json_dict = {}
        # print(row)
        for index in range(1, len(cols)):
            # 判断该值是否为NaN
            if cols[index] == '':
                continue
            if not pd.isna(getattr(row, cols[index])):
                # 内容不是数字，直接删掉
                if judge_number.judge_number(getattr(row, cols[index])):
                    num = str2number.str_number(getattr(row, cols[index]))
                    json_dict[str(getattr(row, cols[0])) + "," + str(cols[index])] = num
        # 判断字典是否为空
        if json_dict:
            json_list.update(json_dict)

    return json_list


def save_json(json_list, save_path):
    # json_list = json_inputs(open_path)
    with open(save_path, "w", encoding="utf-8") as fw:
        # 解决中文编码问题
        json.dump(json_list, fw, ensure_ascii=False,indent=4)


# 传过来excel文件路径，输出文件路径
# 得到json结构：公司名：年份：（表名）：行列：值
if __name__ == '__main__':
    open_path = r'F:\PythonProject\OCRTest\paddleocr\output\2023871650546\[197, 251, 1197, 1789]_0.xlsx'
    save_path = './json/test.json'
    json_inputs(open_path)
