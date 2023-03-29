import logging
from flask import Flask
from apps.article import article_bp
from apps.users import user_bp
from exts import db, cache
# from exts import bootstrap
from settings import DevelopmentConfig


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(DevelopmentConfig)
    # 初始化db
    db.init_app(app=app)

    # 初始化redis
    config_for_redis = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': '10.0.0.21',
        'CACHE_REDIS_PORT': 6379
    }
    cache.init_app(app, config_for_redis)

    # 初始化bootstrap
    # bootstrap.init_app(app=app)

    # 注册蓝图
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(article_bp, url_prefix='/article')
    print(app.url_map)

    # 配置logger
    logger = logging.getLogger(__name__)  # __name__等于apps，app.logger的name也为apps <用logger.name可以查看>
    # basicConfig配置基本属性
    # logging.basicConfig(filename='log.txt', filemode='a', level=logging.WARNING,
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.WARNING)
    logger.setLevel(level=logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

    fh = logging.FileHandler("log.txt",encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return app
