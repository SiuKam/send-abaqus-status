# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import sys
import subprocess

# 可实时返回终端输出
def run_shell(shell):
    cmd = subprocess.Popen(shell, stdin=subprocess.PIPE, stderr=sys.stderr, close_fds=True,
                           stdout=sys.stdout, universal_newlines=True, shell=True, bufsize=1)
    cmd.communicate()
    return cmd.returncode

# 分割输入job列表
fileList = sys.argv[1].split(',')

for fileName in fileList:
    print('===========abaqus analysis begin===========')
    # abaqus运行命令，按需修改
    abqCommand = 'abq2020 job=' + fileName + ' cpus=22 interactive ask_delete=OFF'
    print(run_shell(abqCommand))
    print('===========abaqus analysis end===========')
    
    
    print('===========abaqus alert launch===========')
    # 读取status文件
    staName = fileName + '.sta'
    statFile = open(staName, 'r')
    lines = statFile.readlines()
    # 选取文件后两行，按需选取
    mailContent = '<p>' + lines[-3] + '<br>' + lines[-1] + '</p>'
    # 收发件信息
    message = Mail(
        from_email='from@email.com',
        to_emails='to@email.com',
        subject=lines[-1],
        html_content=mailContent)
    try:
        # 替换SendGrid API Key
        sg = SendGridAPIClient('SendGridApiKey')
        response = sg.send(message)
        print('alert mail sent')
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e.message)

    print('===========abaqus alert finish===========')
