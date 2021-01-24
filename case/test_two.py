import pytest
from util.common import *

@pytest.fixture()
def return_data():
    print("return_data执行前置")
    return 19


@pytest.fixture()
def yield_data():
    print("yield_data执行前置")
    yield 19
    print("yield_data执行后置")


class TestCase(object):

    def test_1(self, return_data):
        print("test_1测试函数中的")
        assert return_data == 19

    def test_2(self, yield_data):
        print("test_2测试函数中的")
        assert yield_data == 19



