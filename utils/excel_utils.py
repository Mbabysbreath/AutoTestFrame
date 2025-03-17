import openpyxl
from config.config import *
def read_excel():
    #1.打开excel文件,参数是文件路径
    workbook=openpyxl.load_workbook(EXCEL_FILE)
    #2.选择表
    worksheet=workbook[SHEET_NAME]
    #3.读取数据,zip函数可以把可迭代对象打包成一个个元组
    data=[]
    keys=[cell.value for cell in worksheet[2]]
    for row in worksheet.iter_rows(min_row=3,values_only=True):
        dict_data=dict(zip(keys,row))#key-value组装
        if dict_data["is_true"]:
            data.append(dict_data)#组装整个列表方便后续传入paramertrize中
    #4.关闭excel文件
    workbook.close()
    return data
print(read_excel())