from flask import Blueprint

# 创建蓝图对象
user_bp = Blueprint('user',__name__)

# 导入蓝图视图函数
from . import user_view