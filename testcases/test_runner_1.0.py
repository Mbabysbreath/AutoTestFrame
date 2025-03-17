import logging

import allure
import jsonpath
import pymysql
import pytest
import requests
from jinja2 import Template
from utils.excel_utils import read_excel
class TestRunner:
    #读测试数据
    data=read_excel()
    #提取后的数据需要初始化一个全局的属性来保存，可以使用{}空字典
    all={}
    #提取后的数据需要初始化一个全局的属性来保存，可以使用{}空字典
    @pytest.mark.parametrize ("case",data)
    def test_case(self,case):
        logging.info(case)
        allure.dynamic.feature(case["feature"])
        allure.dynamic.story(case["story"])
        allure.dynamic.title(f"ID:{case['id']}-{case['title']}")
        method=case["method"]
        url="http://192.168.10.131:8888/api/private/v1"+case["path"]
        headers=eval(case['headers']) if isinstance(case['headers'],str) else None
        params=eval(case['params']) if isinstance(case['params'],str) else None
        data=eval(case['data']) if isinstance(case['data'],str) else None
        json=eval(case['json']) if isinstance(case['json'],str) else None
        files=eval(case['files']) if isinstance(case['files'],str) else None
        request_data={
            "method":method,
            "url":url,
            "headers":headers,
            "params":params,
            "data":data,
            "json":json,
            "files":files
        }
        print(request_data)
        #发起请求，得到响应结果
        res=requests.request(**request_data)
        #断言处理
        if case["check"]:
            assert jsonpath.jsonpath(res.json(),case["check"])==case["expected"]
        else:
            assert case["expected"] in res.text
        #数据库断言
        if case["sql_check"] and case["sql_expected"]:
            conn=pymysql.Connect(
                host="127.0.0.1",
                port=3306,
                database="mydb",
                user="root",
                password="123456",
                charset="utf8"
            )
            cur=conn.cursor()
            cur.execute(case["sql_check"])
            result=cur.fetchone()
            cur.close()
            conn.close()
            assert result[0]==case["sql_expected"]

        #提取
        #引用全局的all
        all=self.all
        #根据all的值，渲染case all['TOKEN']="xxx",{"Authorization":"{{TOKEN}}"}
        case=eval(Template(str(case)).render(all))
        #json提取
        if case["jsonExData"]:
            #首先把jsonExData的key\value拆开
            for key,value in eval(case["jsonExData"]).items():
                value=jsonpath.jsonpath(res.json(),value)[0]
                all[key]=value
        #数据库提取
        if case["sqlExData"]:
            for key,value in eval(case["sqlExData"]).items():
                conn = pymysql.Connect(
                    host="127.0.0.1",
                    port=3306,
                    database="mydb",
                    user="root",
                    password="123456",
                    charset="utf8"
                )
                cur = conn.cursor()
                cur.execute(value)
                result = cur.fetchone()
                cur.close()
                conn.close()
                value=result[0]
                all[key]=value





