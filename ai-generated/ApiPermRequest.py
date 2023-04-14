from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import yaml


class ApiPermRequest:
    def __init__(self, config_path="conf/config.yml", driver_path="chromedriver.exe"):
        with open(config_path, 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)["main_env"]
            except yaml.YAMLError as exc:
                print(exc)
        self.driver_path = driver_path
        self.api_list = self.config["graph_api_list"]

    def request(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument("--disable-extensions")
        options.add_argument('--headless')
        driver = webdriver.Chrome(self.driver_path, options=options)

        url = "https://login.microsoftonline.com/common/adminconsent?client_id={}".format(
            self.config["client_id"])
        driver.get(url)
        driver.implicitly_wait(3)

        # 等待用户登录，需要手动输入用户名和密码
        element_present = EC.presence_of_element_located(
            (By.NAME, 'loginfmt'))
        WebDriverWait(driver, 600).until(element_present)

        # 同意所有请求的权限
        agree_button = driver.find_element_by_id("idBtn_Accept")
        agree_button.click()

        # 保存授权时间
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        perm_file_name = "{}_graph_api_permission.yml".format(now)
        with open(os.path.join(self.config["config_folder"], perm_file_name), "w") as f:
            yaml.dump(self.api_list, f)
