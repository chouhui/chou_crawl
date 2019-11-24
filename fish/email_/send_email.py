#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务


def send_email(meg):
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "cyhimp@163.com"  # 用户名
    mail_pass = "cyh951016"  # 口令

    sender = 'cyhimp@163.com'
    receivers = ['cyhimp@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    cc_mail = ['512991349@qq.com']

    message = MIMEText(meg, 'plain', 'utf-8')
    message['From'] = 'ustc' + receivers[0]
    message['To'] = receivers[0]
    message['Cc'] = cc_mail[0]

    subject = '软件学院新闻通知'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers+cc_mail, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException as e:
        print "Error: 无法发送邮件"
        print e