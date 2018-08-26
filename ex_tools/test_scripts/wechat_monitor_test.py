# coding=utf-8
"""Test - wechat monitor"""

from ex_tools.status_monitor import status_monitor_on_wechat


@status_monitor_on_wechat
def test_function_1(input_num):
    """Test function 1"""
    return input_num + 1


@status_monitor_on_wechat
def test_function_2(input_num):
    """Test function 2"""
    return input_num - 1


@status_monitor_on_wechat
def test_function_3(input_num):
    """Test function 3"""
    _res = test_function_1(input_num)
    return test_function_2(_res)


@status_monitor_on_wechat
def test_function_4(input_num):
    """Test function 4"""
    return input_num / 0


@status_monitor_on_wechat
def test_function_5(input_num):
    """Test function 5"""
    return test_function_4(input_num)


if __name__ == '__main__':
    test_num = 0
    test_function_1(test_num)
    test_function_2(test_num)
    test_function_3(test_num)
    try:
        test_function_4(test_num)
    except Exception as e:
        print(e)
    test_function_5(test_num)
