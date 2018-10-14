from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import Length, DataRequired, Email, ValidationError

from app.models import User, Role


class EditProfileForm(FlaskForm):
    '''
    编辑资料表单
    '''
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('确认')


class EditProfileAdminForm(FlaskForm):
    '''
    管理员编辑资料表单
    '''
    email = StringField('邮箱',validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    confirmed = BooleanField('是否确认')
    role = SelectField('Role', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('确认')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        # selectField 必须在choice属性中设置各选项
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user


    def validate_email(self, field):
        '''
        验证邮箱
        :param field: 邮箱
        :return:
        '''
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_username(self, field):
        '''
        验证用户名
        :param field: 用户名
        :return:
        '''
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')


class PostForm(FlaskForm):
    body = PageDownField('想写点什么', validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('提交')

