#!/bin/env python
#-*-coding:utf-8-*-


import sendmail
import os, time


def iplist(file):                 # 使用生成器产生列表
    for line in file:
        line_list = line.strip()
        yield line_list


def data(**kwargs):
    timeaddi = time.strftime('%Y%m%d%H')
    f= open("/net/apmonitor/client/client" + timeaddi + ".txt","r")
    # f = open('os.path.dirname(os.path.abspath(""))', 'r')
    lis = list(iplist(f))
    for a, b in enumerate(lis):
        if '--------------' in b:
            li = lis[a + 1:]
    for j in li:
        kwargs.setdefault(j[31:44],[]).append(j[83:89])
    return kwargs

# print data()

def check(a):
    v = data().get(a)
    # print v
    try:
        if v.count('144.5M')+v.count(' 72.5M')  < (len(v)/2):
            return a, 0  # AP不正常
        else:
            return a, 1  # AP正常
    except AttributeError:
        return a, 2   # AP下无5G用户


ap = ['BW5-AP-1F01/2','BW5-AP-1F02/2','BW5-AP-1F03/2','BW5-AP-1F04/2','BW5-AP-1F06/2','BW5-AP-1F07/2','BW5-AP-1F08/2', 'BW5-AP-1F09/2','BW5-AP-1F10/2' ,
      'BW5-AP-2F02/2','BW5-AP-2F04/2','BW5-AP-2F05/2','BW5-AP-2F07/2','BW5-AP-2F08/2','BW5-AP-2F09/2','BW5-AP-2F10/2', 'BW5-AP-2F11/2',
      'BW5-AP-3F01/2','BW5-AP-3F02/2','BW5-AP-3F03/2','BW5-AP-3F04/2','BW5-AP-3F05/2','BW5-AP-3F06/2','BW5-AP-3F07/2','BW5-AP-3F08/2','BW5-AP-3F09/2','BW5-AP-3F10/2','BW5-AP-3F11/2',
      'BW5-AP-B103/2','BW5-AP-B104/2','BW5-AP-B105/2','BW5-AP-B106/2','BW5-AP-B107/2', 'BW5-AP-B108/2','BW5-AP-B109/2','BW5-AP-B110/2']
# print list(map(check,ap))
cap = []
dap = {}
for i, j in list(map(check,ap)):
    # print i,j
    if j == 0:
        print i, "请登录AC查询此AP客户端状态！"
        cap.append(i)
        dap.setdefault(i,data().get(i))

# print cap
if len(dap) != int(0):
    sendmail.sendmail(dap)

