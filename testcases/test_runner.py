import logging
import pytest
from jinja2 import Template
from utils.allure_utils import allure_init
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.excel_utils import read_excel
from utils.extractor import json_extractor, jdbc_extractor
from utils.send_request import send_http_request


class TestRunner:
    #读测试数据
    data=read_excel()
    #提取后的数据需要初始化一个全局的属性来保存，可以使用{}空字典
    all={}
    #提取后的数据需要初始化一个全局的属性来保存，可以使用{}空字典
    @pytest.mark.parametrize ("case",data)
    def test_case(self,case):

        # 引用全局的all
        all = self.all
        # 根据all的值，渲染case all['TOKEN']="xxx",{"Authorization":"{{TOKEN}}"}
        case = eval(Template(str(case)).render(all))
        logging.info(f"0.用例ID:{case['id']} 模块:{case['feature']} 场景:{case['story']} 标题:{case['title']}")
        #初始化测试报告
        allure_init(case)
        #解析用例数据
        request_data=analyse_case(case)
        #发起请求，得到响应结果
        res=send_http_request(**request_data)
        #断言处理
        http_assert(case,res)
        #数据库断言
        jdbc_assert(case)
        #提取
        #json提取
        json_extractor(case,all,res)
        #数据库提取
        jdbc_extractor(case,all)





