import pytest,os,sys,json
p=os.path.join(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(p)
from common.public import *
from common.data import *
from base.method import Requests
from utils.operationExcel import OperationExcel

obj = Requests()
objYaml = OperationExcel()
dataobj = Isecd()

@pytest.mark.parametrize('datas', objYaml.readExcel('testdata.xlsx'))
def test_001(datas):
    test_001.__doc__ = datas["Description"]
    print("请求参数：" + "\n" + str(datas["Data"]))
    r = obj.post(
        url = datas["Url"],
        headers = datas["Header"],
        json = datas["Data"]
    )
    if datas["ExpectData"] == "database":
        subjectId = datas["Data"]["data"]["courseId"]
        teacherId = datas["Data"]["data"]["teacherId"]
        grdId = datas["Data"]["data"]["collegeId"]
        min = datas["Data"]["data"]["minToClassRate"]
        max = datas["Data"]["data"]["maxToClassRate"]
        startTime = datas["Data"]["data"]["startTime"]
        endTime = datas["Data"]["data"]["endTime"]
        lessnum = datas["Data"]["data"]["sectionId"]
        result = dataobj.stucountdetail(startTime,endTime,grdId,subjectId,teacherId,lessnum,min,max)
        print("数据库查询结果：" + "\n" + str(result))
        print("接口返回结果：" + "\n" + str(r.json()))
        assert str(r.json()['total']) == str(len(result))
    assert str(r.json()['result']) == datas['ExpectResult']
    assert str(r.json()['message']) == datas['ExpectMessage']
if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_dc.py"])

