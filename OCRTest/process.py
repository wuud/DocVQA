import shutil
import sys
import pdfplumber
from OCRTest.excel2json import *
from OCRTest.pdf_check import *
from OCRTest.remove_seal_main import *
import os
import re
import cv2
from OCRTest.util import str2number
from OCRTest.util import judge_number
from OCRTest.paddleocr import PPStructure, draw_structure_result, save_structure_res
from PIL import Image
import time

def remove_dir(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    else:
        shutil.rmtree(filepath)
        os.makedirs(filepath)


def main_process(pdf_path, page_start, page_end):
    start_time = time.time()
    pdf_path = pdf_path.name
    print(pdf_path)
    page_start = int(page_start)
    page_end = int(page_end)
    final_dict = {}
    pdf2imagepath = "./OCRTest/pdf2image/"
    no_seal_image_path = "./OCRTest/dealed_image/"
    # json保存路径为json目录下公司名与年份名的拼接
    save_json_path = './OCRTest/json/'
    cur_time = time.localtime()
    # 创建此次任务的文件名前缀
    path_prefix = str(cur_time.tm_year) + str(cur_time.tm_mon) + str(cur_time.tm_mday) + str(cur_time.tm_hour) + \
                  str(cur_time.tm_min) + str(cur_time.tm_sec)

    pages = []
    for i in range(page_start - 1, page_end):
        pages.append(i)

    # 使用正则表达式提取文件名中的年份和公司名称
    filename = os.path.basename(pdf_path).split('.')[0]
    p = r"\d{4}"
    pattern = re.compile(p)
    year = pattern.findall(filename)
    if not year:
        print('请将文件名修改为公司名与年份的组合！')
        sys.exit(0)
    # 文件年份
    year = year[0]
    # 公司名称
    company = ""
    for c in filename:
        if c.isdigit():
            break
        else:
            company += c
    print(company)
    print(year)
    save_json_path = save_json_path + company + year + ".json"
    is_electronic = is_electronic_pdf(pdf_path)
    if is_electronic:
        print("这是电子版PDF")
        # TODO 存在多个表key相同的情况
        json_list = {}
        with pdfplumber.open(pdf_path) as pdf:
            common_col = []
            common_table_name = ''
            for page in pages:
                cur = pdf.pages[page]
                # 获取当前页的所有文本
                text = cur.extract_text()
                text_list = text.split("\n")
                table_name = [s for s in text_list if '资产负债表' in s or '利润表' in s or '现金流量表' in s]
                # print(table_name)
                # 获取当前页的所有表格
                table_list = cur.extract_tables()
                # print(table_list)
                # 遍历每一张表
                for table in table_list:
                    cols = table[0]
                    len_col = len(cols)
                    # for c in range(len_col):
                    #     common_col.append('第' + str(c) + '列')
                    # 判断当前行是否为第一行
                    # 也就是确定表头
                    if common_table_name == '':
                        if len(table_name) != 0:
                            common_table_name = table_name[0]

                    if not common_col:
                        common_col = cols
                    else:
                        flag = True
                        for i in range(1, len(cols)):
                            if cols[i] == '' or judge_number.judge_number(cols[i]):
                                flag = False
                                break
                        if flag:
                            common_col = cols
                            if len(table_name) != 0:
                                common_table_name = table_name[0]
                    # print(cols)
                    print("---------------" + " ".join(common_col) + "------------------")
                    for i in range(1, len(table)):
                        # print(table_list[i][0])
                        table[i][0] = table[i][0].replace('\n', '')
                        for j in range(1, len(common_col)):
                            if table[i][j] == '' or table[i][j] is None:
                                continue
                            key = common_table_name + "," + table[i][0] + "," + common_col[j]
                            value = table[i][j]
                            if judge_number.judge_number(value):
                                num = str2number.str_number(value)
                                json_list[key] = num
                            # print(key + " " + value)
        year_dict = {}
        year_dict[year] = json_list
        company_dict = {}
        company_dict[company] = year_dict
        print(company_dict)
        save_json(company_dict, save_json_path)
        final_dict = company_dict
    else:
        print("这是扫描图像版PDF")
        print("-----------将pdf指定页码转换为图片 Start-------")
        pdf_image(pdf_path, pdf2imagepath, pages, path_prefix)
        print("-----------将pdf指定页码转换为图片 End---------")
        print("---------------去除印章 Start---------------")
        files = os.listdir(pdf2imagepath)
        for pg in pages:
            file_path = os.path.join(pdf2imagepath, path_prefix + str(pg) + ".png")
            print(file_path)
            if os.path.isfile(file_path):
                seal_remove(file_path)
        print("---------------去除印章 End---------------")
        print("---------------图片OCR Start-------------")
        files = os.listdir(no_seal_image_path)
        table_engine = PPStructure(show_log=True)
        for pg in pages:
            file_path = os.path.join(no_seal_image_path, path_prefix + str(pg) + ".png")
            if os.path.isfile(file_path):
                save_folder = './OCRTest/paddleocr/output'
                img = cv2.imread(file_path)
                result = table_engine(img)
                save_structure_res(result, save_folder, os.path.basename(file_path).split('.')[0])

                for line in result:
                    line.pop('img')

                font_path = './OCRTest/paddleocr/doc/fonts/simfang.ttf'  # PaddleOCR下提供字体包
                image = Image.open(file_path).convert('RGB')
                im_show = draw_structure_result(image, result, font_path=font_path)
                im_show = Image.fromarray(im_show)
                im_show.save('./OCRTest/paddleocr/result.jpg')
        print("---------------图片OCR End-------------")

        # 将excel内容转换为json文件
        print("---------------Excel to Json Start-------------")
        filelist = []
        json_total = {}
        for pg in pages:
            path = './OCRTest/paddleocr/output/' + path_prefix + str(pg)
            for normal_file in os.listdir(path):
                if '.xlsx' == os.path.splitext(normal_file)[1]:
                    # 遍历上述文件夹，调用excel2json方法
                    json_list = json_inputs(path + "/" + normal_file)
                    json_total.update(json_list)
        # 将结果放入company year组成的字典中
        year_dict = {}
        year_dict[year] = json_total
        company_dict = {}
        company_dict[company] = year_dict
        save_json(company_dict, save_json_path)
        final_dict = company_dict
        print("---------------Excel to Json End-------------")
    remove_dir(pdf2imagepath)
    # remove_dir(no_seal_image_path)
    remove_dir("./OCRTest/paddleocr/output")
    end_time = time.time()
    print("程序运行时间:{}s".format(end_time - start_time))
    return final_dict
