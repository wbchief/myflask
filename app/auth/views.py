from flask import flash
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.utils import redirect

from app.auth import auth
from app import create_app, db
from app.auth.form import LoginForm, RegisterationForm, ChangePasswordForm, PasswordResetRequestForm, \
    PasswordResetForm, ChangeEmailForm
from app.emails import send_email
from app.models import User, Permission

app = create_app('testing')

@app.context_processor
def include_permission_class():
    return {'Permission': Permission}

@app.route('/')
def index():
    return '<h2> 欢迎 </h2>'

@auth.before_app_request
def before_request():
    if current_user.is_authenticated: # 判断用户是否登录
        current_user.ping()
        if not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_authenticated or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    '''
    登录，
    :return:
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 在用户会话中标记用户已登陆
            login_user(user, form.remeber_me.data)
            next = request.args.get('next')
            print(1, next)
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
                # print(2, next)
                # print(3, next)
            return redirect(next)
        flash('你的用户名或密码好像有点问题哦')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    '''
    退出
    :return:
    '''
    logout_user() #删除并重设会话
    flash('你已经退出喽.')
    #print('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    '''
    用户注册，并给所注册email发送验证邮件
    :return:
    '''
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '请确认你的帐号',
                   'auth/email/confirm', user=user, token=token)

        flash('一封确认邮件已经发到你的邮箱喽，请注意查收呀.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    '''
    确认用户的账户
    :param token:
    :return:
    '''
    if current_user.confirmed:
        print(current_user.email)
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('你已经验证完喽. 谢谢!')
        #print('You have confirmed your account. Thanks!')
    else:
        flash('确认链接无效或已过期')
        #print('The confirmation link is invalied or has expired')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('修改密码成功')
            print('修改密码成功')
        else:
            flash('旧密码不正确')
            print('旧密码不正确')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    '''
    密码重置请求
    :return:
    '''
    if not current_user.is_anonymous:
        return render_template('main.index')
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置你的密码',
                       'auth/email/reset_password', user=user, token=token)
        flash('一封指示重置密码的电子邮件已经发送给你')
        #print('An email with instructions to reset your password has been sent to you')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
   #print('1111111111111111111111111111111111111111111111111111111111111')
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('你的密码已经重置')
            #print('你的密码已经重置')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/password_reset.html', form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '请确认你的邮箱地址', 'auth/email/change_email', user=current_user, token=token)
            flash('一封带有确认你新邮箱地址说明的邮件已经发送给你')
            return redirect(url_for('main.index'))
        else:
            flash('不合法的邮箱或密码')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    '''

    :param token:
    :return:
    '''
    if current_user.change_email(token):
        db.session.commit()
        flash('你的邮箱已经修改')
    else:
        flash('不合法的请求')
    return render_template(url_for('main.index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')