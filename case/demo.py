import time
from functools import reduce
from ddt import ddt, data
import unittest
# from util.request import Request
# request = Request()
from util.common import *
from util.mysql import MysqlDb


# url = "http://192.168.137.1:9528/dev-api/account/login"
# data = '{"username": "wangjinliang", "password": "wang494195"}'
# r = request.post_request(url, data)
# print(r.text)
# cookie = r.json()["data"]["token"]
#
# url = "http://192.168.137.1:9528/dev-api/shop/category/list"
# data = '{"page": 1, "limit": 20}'
# headers = {"Authorization": cookie}
# r = request.get_request(url, data, headers=headers)
# print(r.text)
#
# url = "http://192.168.137.1:9528/dev-api/shop/category"
# data = {"name": "iphone3"}
# headers = {"Authorization": cookie}
# # headers = str(headers)
# r = request.post_request(url, data, headers=headers)
# print(r.text)
#
# url = "http://192.168.137.1:9528/dev-api/file"
# headers = {"Authorization": cookie}
# r = request.post_request_multipart(url, file_name='fanzuimao', headers=headers)
# print(r.text)

# def where_sql_deal(iterable, str=","):
#     if len(iterable) == 1:
#         value = iterable[0].split("=")[1]
#         res = iterable[0].replace(value, f"'{value}'")
#         return res
#     else:
#         res_li = []
#         for i in iterable:
#             value = i.split("=")[1]
#             res = i.replace(value, f"'{value}'")
#             res_li.append(res)
#         return f"{str}".join(res_li)


# {
#     "test_case1": {
#         "key": "value1",
#         "status_code": 200
#     },
#     "test_case2": {
#         "key": "value2",
#         "status_code": 200
#     },
#     "test_case3": {
#         "key": "value3",
#         "status_code": 200
#     }
# }


my = MysqlDb()
a = my.query(table="tp_goods", columns=["goods_id", "goods_name", "goods_sn", "store_count", "comment_count"],
             where=["click_count=20"], order=["goods_id"], one=False)


@ddt
class TestLogin(unittest.TestCase):

    @data(*a) #对li解包
    def test_demo(self, value):	# test_demo只需要一个参数
        print("传入的value是：", value["store_count"])


if __name__ == '__main__':
    unittest.main()
