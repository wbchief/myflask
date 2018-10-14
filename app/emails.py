from threading import Thread

from flask import Flask
from flask import current_app
from flask import render_template
from flask_mail import Mail, Message

from app import mail


def send_async_email(app, msg):
    '''
    异步发送
    :param app:
    :param msg:
    :return:
    '''
    with app.app_context():
        try:

            mail.send(msg)
        except Exception as e:
            mail.send(msg)

        print('发送成功')


def send_email(to, subject, template, **kwargs):
    '''
    发送邮件
    :param to: 接受者
    :param subject: 主题
    :param template: 渲染邮件正文的模板
    :param kwargs: 关键字参数
    :return:
    '''
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJEXT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr