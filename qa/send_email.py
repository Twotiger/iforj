# -*- coding: utf-8 -*
import smtplib
from email.mime.text import MIMEText
from config import MAIL_HOST, MAIL_USER, MAIL_PASS, MAIL_POSTFIX
#mailto_list=["501362431@qq.com"]


def sendMail(to_list,sub,content):  #to_list���ռ��ˣ�sub�����⣻content���ʼ�����

    me="IFORJ"+"<"+MAIL_USER+"@"+MAIL_POSTFIX+">"   #�����hello�����������ã��յ��ź󣬽�����������ʾ
    msg = MIMEText(content,_subtype='html',_charset='utf8')    #����һ��ʵ������������Ϊhtml��ʽ�ʼ�
    msg['Subject'] = sub    #��������
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(MAIL_HOST)  #����smtp������
        s.login(MAIL_USER, MAIL_PASS)
        s.sendmail(me, to_list, msg.as_string())  #�����ʼ�
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == "__main__":
    sendMail(['501362431@qq.com'], 'asdf', '<a href="http:///127.0.0.1/versiton/adfasdf">hit me</a>')
