import pytest

from weibo_search.middlewares import ProxyMiddleware, CookiesMiddleware
from weibo_search.settings import PROXY_URL


class TestProxyMiddleware():
    proxy_middle = ProxyMiddleware(PROXY_URL)

    def test_get_random_proxy(self):
        assert self.proxy_middle.get_random_proxy(), "Proxy url out of date, Connection Error"


