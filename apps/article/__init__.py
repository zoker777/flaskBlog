from flask import Blueprint

# 创建蓝图对象
article_bp = Blueprint('article',__name__,url_prefix='/article')

# 导入蓝图视图函数
from . import article_view