#!/bin/env python
#-*-coding:utf-8-*-

'''
在Python3内测试通过，可群发邮件，自定义内容
'''

import smtplib
from email.mime.text import MIMEText
import string

sender = 'net.srv@guazi.com'
receiver = ['sunshouwen@guazi.com']

b = ' '.join(receiver)
c = b.split('@guazi.com')
d = ','.join(c[:-1])
e = string.capwords(d)

smtpserver = 'mail.guazi-corp.com'
username = 'net.srv@guazi-corp.com'
password = 'qazwsxcde@1314'


def sendmail(ap):
    try:
        message1 = '''Hi,%s:<br>
&nbsp;&nbsp;Please attension the AP : <font color=red>%s</font><br>
&nbsp;&nbsp;The following shows the speed of STAs in the AP or APs above:<br>
        '''% (e, ap.keys())
        message2 = ""
        for i in ap.keys():
            message2 = message2 + "&nbsp;&nbsp;%s : %s\n" % (i, ap.get(i))

        message3 = '''\n\r<font color=green>---------------\nFrom AP monitor center </font><br>
                '''
        html_start = '<font face="Courier New, Courier, monospace"><pre>'
        html_end = '</pre></font>'



        msg = MIMEText(html_start + message1 + message2 + message3 + html_end, _subtype='html', _charset='utf-8')

        # msg = MIMEText('你好','text','utf-8')
        subject = '无线用户连接速率降低，请在各AP下检查用户状态'
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ','.join(receiver)

        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    except IndexError:
        print("无告警AP")


if __name__ == '__main__':
    sendmail({'ap1':['144M', '72.5M'],'ap2':['144.5']})
