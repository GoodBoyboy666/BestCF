import json
import os
import schedule
import time
import pandas

#Linux和Windows的可执行程序命名不同
STFile="CloudflareST.exe"
IPFile="ip.txt"
# 设置需要的域名
AliDDNS_DomainName="xxxx.xxx"
# 设置需要的主机名：ddns
AliDDNS_SubDomainName="xxx"
# 免费版最低为600（10分钟）~86400（1天）
AliDDNS_TTL="600"
# 设置阿里云的Access Key
AliDDNS_AK="xxxxxxxxxxxxxxxxxxx"
# 设置阿里云的Secret Key
AliDDNS_SK="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#每日执行的时间（当然也可以自己根据实际情况修改）
Time="00:00"
#检查间隔
CheckTime=1 #单位为秒
#无需填写
ResultIP=""


# 首先需要安装阿里云的Python SDK，可以通过pip install aliyun-python-sdk-core aliyun-python-sdk-alidns==3.0.7进行安装

########################################以下代码为ChatGPT所写##########################################

from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest, UpdateDomainRecordRequest 

def update_dns_record(DomainName, RR, Type, Value):
    # 创建AcsClient实例
    client = AcsClient(AliDDNS_AK, AliDDNS_SK, 'cn-hangzhou')

    # 创建一个DescribeDomainRecordsRequest并设置参数
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(DomainName)

    # 发起请求，得到每条记录的详细信息
    response = client.do_action_with_exception(request)
    data = json.loads(response)

    # 遍历每条记录，找到需要修改的记录
    for record in data['DomainRecords']['Record']:
        if record["RR"] == RR:
            if record["Value"]==ResultIP:
                print("IP无需更新")
                break
            # 创建一个UpdateDomainRecordRequest，并设置参数
            request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
            request.set_RecordId(record["RecordId"])
            request.set_RR(RR)
            request.set_Type(Type)
            request.set_Value(Value)

            # 发起请求
            response = client.do_action_with_exception(request)
            print ("Update record success")
            break
        
################################################################################################

print("欢迎使用阿里云自动解析脚本")

print("开始检查必需文件……")

if not os.path.exists(STFile):
    print("未找到CloudflareST")
    exit(1)
    
if not os.path.exists(IPFile):
    print("未找到IP文件！")
    exit(1)
    
print("检查完毕")

def changeDNS():
    update_dns_record(AliDDNS_DomainName, AliDDNS_SubDomainName, 'A',ResultIP)

def getIP():
    global ResultIP
    data=pandas.read_csv("result.csv")
    if not (data.iloc[0,0]=="" or data.iloc[0,0]==ResultIP):
        ResultIP=data.iloc[0,0]
        changeDNS()

def testIP():
    os.system(STFile+" -f "+IPFile+" -p 0")  #可以自己定制命令
    print("测速完成")
    getIP()
    
#设置启动时间（时间间隔切勿小于每次测速所需要的时间，否则会有很可怕的事情发生）
#格式参考https://blog.csdn.net/liao392781/article/details/80521194
schedule.every().day.at(Time).do(testIP) 

while True:
    schedule.run_pending()
    time.sleep(CheckTime)  #检查间隔

