import ast
import json
import os
import configparser


def get_full_file_name(file_name, path="../data/"):
    '''
    根据文件名模糊匹配文件，返回带后缀完整文件名
    :param file_name:
    :param path:
    :return:
    '''
    files = os.listdir(path)
    for item in files:
        if item.split('.')[0] in file_name:
            return item, path

        else:
            print("文件不在当前目录：", os.path.abspath(path))


def get_file_suffix(file_name, path="../data/"):
    '''
    根据文件名模糊匹配文件，返回文件后缀
    :param file_name:
    :param path:
    :return:
    '''
    files = os.listdir(path)
    for item in files:
        if file_name in item:
            file_suffix = os.path.splitext(item)[-1]
            return file_suffix, path
        else:
            print("文件不在当前目录：", os.path.abspath(path))


def check_file_suffix(full_file_name, path="../data/"):
    '''
    校验当前文件后缀是否正确
    :param full_file_name:
    :param path:
    :return:
    '''
    file_name = full_file_name.split('.')[0]
    file_suffix = full_file_name.split('.')[1]
    real_file_suffix = get_file_suffix(file_name, path=path)[0]
    if file_suffix not in real_file_suffix:
        print(f"{full_file_name}后缀错误，正确后缀为{real_file_suffix}")
    else:
        return full_file_name, path


def format_data(data):
    '''
    兼容接口入参类型，转为dict类型
    :param data:
    :return:
    '''
    if data is not None and type(data) is not dict:
        data = json.loads(data)
        return data
    else:
        return data


def json_deal(cont):
    '''
    处理json中true,false,null,转为python对应的数据类型
    :param cont:
    :return:
    '''
    return cont.replace("true", "True").replace("false", "False").replace("null", "None")


def single_quotes_deal(cont):
    '''
    json中如果存在单引号，loads反序列化会失败，特殊方法处理
    :param cont:
    :return:
    '''
    cont = json_deal(cont)
    if "'" in cont:
        return ast.literal_eval(cont)
    else:
        pass


def read_conf(conf_name="conf.ini", option="mysql"):
    cfp = configparser.ConfigParser()
    cfp.read("../config/" + conf_name, encoding="utf-8")
    return cfp[option]


def include_symbol(iterable):
    symbol = ["=", ">", "<", "!=", ">=", "<=" "between"]
    for j in symbol:
        if j in iterable:
            return j


def sql_deal(iterable, str=","):
    if len(iterable) == 1:
        if "'" in iterable[0]:
            return iterable[0]
        else:
            j = include_symbol(iterable[0])
            value = iterable[0].split(j)[1]
            res = iterable[0].replace(value, f"'{value}'")
            return res
    else:
        res_li = []
        for i in iterable:
            j = include_symbol(i)
            value = i.split(j)[1]
            if "'" in value:
                res_li.append(i)
            else:
                res = i.replace(value, f"'{value}'")
                res_li.append(res)
        return f"{str}".join(res_li)


if __name__ == '__main__':

    pass

