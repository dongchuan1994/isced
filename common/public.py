import os,sys,json,base64
sys.path.append("C:\\Users\\DONGCHUAN\\AppData\\Roaming\\Python\\Python37\\site-packages")
import yagmail

def filePath(fileDir='data',fileName='login'):
    '''
    :param fileDir:文件目录
    :param fileName:文件名称
    :param return:返回文件绝对路径
    '''
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)), #获取上一级目录,并拼接成绝对路径
        fileDir,
        fileName
    )

def mkdir(path):
	if not os.path.exists(path):                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)             #makedirs 创建文件时如果路径不存在会创建这个路径

def getUrl():
    with open(filePath("config","config.json"),'r') as f:
        data = json.loads(f.read())
        if data['port'] == '':
            return data['url']
        else:
            return data['url'] + ':' + data['port']

def getOrgCode():
    with open(filePath("config","config.json"),'r') as f:
        data = json.loads(f.read())
        return data['orgcode']

def sendEmail():
    yag = yagmail.SMTP(user='873555954@qq.com',
                       password='wauswyjovrklbbeh',
                       host='smtp.qq.com',
                       port='465')

    body = "测试报告:http://10.4.2.240:8080/job/apiTest/ws/report/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A.html"

    yag.send(to=['1134417759@qq.com'],
             subject='测试报告',
             contents=[body])

