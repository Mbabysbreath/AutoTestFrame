#utils/extractor.py
import logging

import allure
import jsonpath
from utils.send_request import send_jdbc_request
def json_extractor(case,all,res):
    if case["jsonExData"]:
        # 首先把jsonExData的key\value拆开
        with allure.step("4.JSON提取"):
            for key, value in eval(case["jsonExData"]).items():
                value = jsonpath.jsonpath(res.json(), value)[0]
                all[key] = value
            logging.info(f"4.JSON提取,根据{case['jsonExData']}提取数据,此时全局变量是all={all}")
def jdbc_extractor(case,all):
    if case["sqlExData"]:
        with allure.step("4.JDBC提取"):
            for key, value in eval(case["sqlExData"]).items():
                value = send_jdbc_request(value)
                all[key] = value
            logging.info(f"4.JDBC提取,根据{case['sqlExData']}提取数据,此时全局变量是all={all}")