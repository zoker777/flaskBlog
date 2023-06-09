import os


class Config:
    DEBUG = True
    # mysql+pymysql://user:password@hostip:port/databasename
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flaskblog'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@10.0.0.21:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
    # 项目路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 静态文件夹的路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    # 头像的上传目录
    UPLOAD_ICON_DIR = os.path.join(STATIC_DIR, 'upload/icon')
    # 相册的上传目录
    UPLOAD_PHOTO_DIR = os.path.join(STATIC_DIR, 'upload/photo')

class DevelopmentConfig(Config):
    ENV = 'development'


class ProductionConfig(Config):
    ENV = 'production'
    DDEBUG = False


if __name__ == '__main__':
    print(Config.BASE_DIR)
    # print(os.path.abspath(__file__))
    print(Config.STATIC_DIR)
    print(Config.UPLOAD_ICON_DIR)
