#!/bin/env python
#-*-coding:utf-8-*-
import emails


def sendmail(address, ap):
    try:
        m = emails.html(text = u'''Please attension the AP/APs :%s. \n\rExample is: \n\r 'show ac-config client | inc %s'
                            '''%(ap, ap[0]),
                             subject=u'无线用户连接速率降低，请在各AP下检查用户状态 %s'% ap,
                             mail_from=(u'告警邮箱',
                                        'net.srv@guazi.com'))
        r = m.send(to = (address),
                        smtp={'host':'mail.guazi-corp.com',
                              'user': 'net.srv@guazi-corp.com',
                              'password': 'qazwsxcde@1314'})
        if r.status_code == 250:
            print "邮件发送成功！"
    except IndexError:
        print "无告警AP"


if __name__ == '__main__':
    sendmail('sunshouwen@guazi.com', ['AP1', 'ap2'])

