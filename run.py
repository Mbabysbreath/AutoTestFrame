import os

import pytest
if __name__=="__main__":
    # pytest.main(["参数1","参数2"])
    pytest.main(["-sv","--html=report/report.html","./testcases/test_runner.py","--alluredir","./report/json_report","--clean-alluredir"])
    os.system("allure generate ./report/json_report -o ./report/html_report --clean")
