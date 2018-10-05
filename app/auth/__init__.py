'''
auth蓝本在全局作用中定义路由
'''
from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.auth import views