from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# 下面必须导入所有db对象，否则执行python3 app.py db migrate不生效
from apps.users.model import *
from apps.article.model import *
from apps import create_app
from exts import db

app = create_app()


# 用manager接管app，使得可以通过部分shell命令调用此flask app
manager = Manager(app=app)
# 绑定app和db
migrate = Migrate(app=app, db=db)
# 添加一个shell命令来操作db
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
