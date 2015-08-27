# -*- coding: utf-8 -*
import smtplib
from email.mime.text import MIMEText
from config import MAIL_HOST, MAIL_USER, MAIL_PASS, MAIL_POSTFIX
#mailto_list=["501362431@qq.com"]


def sendMail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容

    me="IFORJ"+"<"+MAIL_USER+"@"+MAIL_POSTFIX+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(MAIL_HOST)  #连接smtp服务器
        s.login(MAIL_USER, MAIL_PASS)
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == "__main__":
    sendMail(['501362431@qq.com'], 'asdf', '<a href="http:///127.0.0.1/versiton/adfasdf">hit me</a>')
