import pytest
from weibo_search.account_build.login import WeiboLogin


def test_get_cookie():
    """This test weibo login, needs process the window to make sure the test is right"""
    weibo_login = WeiboLogin('wang198907chen884@163.com', 'Qh23955766CC')
    cookie_txt = weibo_login.run()
    assert len(cookie_txt) != 0
