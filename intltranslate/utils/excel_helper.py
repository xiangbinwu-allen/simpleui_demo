import json
import os
import re
from os.path import isfile

from openpyxl import load_workbook, Workbook


def _convert_excel_2_dict(file_path):
    dic = {}
    work_book = load_workbook(file_path)
    sheetnames = work_book.sheetnames
    if len(sheetnames) < 1:
        return
    sheet = work_book[sheetnames[0]]
    data_tuple = tuple(sheet.rows)
    for row in data_tuple:
        i = 0
        cell_values = []
        for cell in row:
            cell_values.append(cell.value)
            i += 1
        dic[cell_values[0]] = cell_values[2]
    return dic

def _convert_dict_2_json(json_file_name, dic_list):
    dic_list = {"first": "0",
              "common1.aa": "1",
              "common1.bb": "2",
              "common2.cc": "3",
              "common2.dd": "4",
              "common2.ee.ff": "5",
              "common2.ee.gg": "6",
              "common2.ee.hh": "7",
              "cc": "1"
           }
    # 将dicnew转换为对象
    dic_trun = {}
    conver_dic_2_dics(dic_list, dic_trun)

    # 将数据写入文件
    json_data = json.dumps(dic_trun)
    with open(json_file_name,'wb') as f:
        f.write(json_data)


def conver_dic_2_dics(dic_list, dic_trun):
    for dic in dic_list:
        print(dic)
        print(dic.find("."))
        if dic.find(".") != -1:
            dic_trun_child = {}
            key = dic[:dic.index(".")]
            print(key)
            dic_trun[key] = dic_trun_child
            print(dic[dic.index(".")])
            conver_dic_2_dics(dic[dic.index(".")], dic_trun_child)
            continue
        dic_trun[dic] = dic_list[dic]
    print(dic_trun)


def save_2_excel(file_path, tables):
    if not file_path.endswith(".xlsx"):
        raise ValueError("文件必须为.xlsx结尾的Excel文件")
    work_book = Workbook()
    is_first = True
    for table in tables:
        if is_first:
            ws = work_book.active
            is_first = False
        else:
            ws = work_book.create_sheet()
        # 添加表头
        table_heads = []
        for attr in table[0].__dict__:
            # 过滤"_"开头的属性
            if not attr.startswith("_"):
                table_heads.append(attr)
        ws.append(table_heads)

        # 添加数据
        for row in table:
            data = []
            for head in table_heads:
                data.append(getattr(row, head))
            ws.append(data)
    try:
        # 生成保存文件夹路径
        folder_index = max(file_path.rfind("\\"), file_path.rfind("/"))
        if folder_index != -1:
            folder_path = file_path[0:folder_index]
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
        work_book.save(file_path)
    except Exception:
        raise OSError("创建Excel失败")

def _convert_value(value):
    """
    将单元格中数据，区分基本类型
    类似"true"/"false"(不区分大小写)转换为bool值
    长得像数字的转换为float类型
    其他（空格、空行）转换为None
    :param value: 单元格的值
    :return: 转换后的类型
    """
    value_str = str(value).lower()
    if value_str == 'true':
        return True
    elif value_str == 'false':
        return False
    elif re.match(r"^[+|-]?\d+.?\d*$", value_str):
        return float(value_str)
    elif re.match(r"^\s*$", value_str):
        return None
    else:
        return value


if __name__ == '__main__':
    file_path = os.path.join("C://Users//86136//Desktop//打包//EN-20210726-睿易app拓扑.xlsx")
    file_path2 = os.path.join(os.getcwd(), "templates\\app_file\\zh.json")
    dic={}
    _convert_dict_2_json(file_path2, dic)