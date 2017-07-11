#-*- coding: utf-8 -*-
#!/usr/bin/python
import threading
import urllib2
from conn_type_h3c import SSH
import time,os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def ssh2(host,username,passwd,cmd):
    try:
        ssh = SSH(host, username, passwd)
        # print "hh"
        ssh.connect()
        # print "OK"
        ssh.set_su('Qs3#Px#8U*v6Y')
        return ssh.command(cmd)
        ssh.close()
    except:
        print '%s\tError\n'%(host)

timeTuple = time.localtime()
timeaddi = time.strftime('%Y%m%d%H')
filetime = time.strftime('%Y-%m-%d',timeTuple)
# if __name__=='__main__':
username = "ganji"  #用户名
passwd = "6P&z72M*I%r7"    #密码
threads = []   #多线程
host1 = '192.168.71.201'
cmd1 = 'ter len 0 \n show ac-config client | inc BW5-AP-'  # 你要执行的命令
data = ssh2(host1,username,passwd,cmd1)

output = open("/net/apmonitor/client/client"+ timeaddi + ".txt", "w")
        #output.writelines(jiancha)
output.write(data)
output.close()
