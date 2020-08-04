import os
import sys
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.getcwd())


TEMPLATES_FOLDER = os.getcwd() + '/templates/'


class WeiboLogin:
    def __init__(self, username, password):
        # os.system('pkill -f phantom')
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
        # self.browser = webdriver.PhantomJS()
        self.browser = webdriver.Chrome()
        # self.browser.set_window_size(1050, 840)
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def open(self):
        """
        login with weibo account
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()
        time.sleep(8)

    def run(self):
        """
        :return:
        """
        self.open()
        WebDriverWait(self.browser, 30).until(
            EC.title_is('微博')
        )
        cookies = self.browser.get_cookies()
        cookie = [item["name"] + "=" + item["value"] for item in cookies]
        assert len(cookie) >= 0, 'No Cookie Get'
        cookie_txt = '; '.join(item for item in cookie)
        self.browser.quit()
        return cookie_txt


if __name__ == '__main__':
    file_path = os.getcwd() + '/account.txt'
    print(file_path)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    account_cookies = []
    for line in lines:
        line = line.strip()
        username = line.split('----')[0]
        password = line.split('----')[1]
        print('=' * 10 + username + '=' * 10)
        try:
            cookie_str = WeiboLogin(username, password).run()
        except Exception as e:
            print(e)
            continue
        print('Successfully get cookie')
        print('Cookie:', cookie_str)
        account_cookies.append({"_id": username, "password": password, "cookie": cookie_str, "status": "success"})
    with open(os.getcwd() + '/account_info.pk', 'wb') as f:
        pickle.dump(account_cookies, f)
