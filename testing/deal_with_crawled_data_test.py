"""
This file does unittest for functions in web.deal_with_crawled_data
"""
from web.deal_with_crawled_data import *
import pytest


def test_predict_lock_from_text():
    """Test different texts lock condition"""
    test_txts = ['广州将公共卫生响应级别下调至二级', '北京近日疫情启动一级公共卫生事件响应', '各地疫情相应级别已经下调至三级']
    for i in range(len(test_txts)):
        assert predict_lock_from_text(test_txts[i])[0] == i+1


def test_predict_lock_for_region():

    "Test normal lock condition transition"
    lock, ids = predict_lock_for_region([['a11', 2, 0.0], ['a12', 0, 0.0], ['a13',2, 0.0], ['a14', 3, 0.0]], 3)
    assert lock == 2
    assert ids == ['a11', 'a13']
    "Test lock condition continuation"
    lock, ids = predict_lock_for_region([['a11', 0, 0.0], ['a12', 0, 0.0], ['a13', 0, 0.0], ['a14', 0, 0.0]], 3)
    assert lock == 3
    assert ids == ['a11', 'a12', 'a13', 'a14']




