# 一、flask入门简介
## 1.1. python web全栈介绍：
web 阶段：
python 基础
数据库：mysql redis
网页：html+css+js+jquery+bootstrap
vue：前后分离

Web框架：
vue，jquery，bootstrap
web后端：
flask 轻量级 灵活
tornado c10k  
django 重量级 

## 1.2. 搭建框架:
### 1.2.1 要有虚拟环境:
 linux: virtualenv  virtualenvwrapper<管理和使用虚拟环境更方便>
        配置文件的修改：  .Envs
        .bashrc
        ...


 windows:pip install virtualenvwrapper-win
         mkvirutalenv mytest1  新建虚拟环境
         workon 虚拟环境名
         deactivate  退出虚拟环境
         rmvirutalenv 虚拟环境名

### 1.2.2 新建虚拟环境：
   将项目切换到虚拟环境上

   点击终端:(flaskenv) C:\Users\running\Desktop\GPDay41\代码\day41_flask>
   说明进入到虚拟环境中....

### 1.2.3 flask环境搭建：

app=  Flask(__name__)

#### 1.2.3.1 关联服务器并启动
  app.run(host='',port=5000)

  在终端： python app.py
#### 1.2.3.2 app.route('/')  注册路由
   def func():
      return .....


### 1.2.4 配置：
Environment: production
 production   ----》 正在
 development  ---》开发
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
  Debug mode: off

debug mode:on
run(deubg=True)  ----> mode:on
on的模式： 代码有改变则服务器重启（重新加载程序）

- 配置解耦：
```
    settings.py:
        ENV = 'development'
        DEBUG = True
    在app启动前引入文件(两种)：
        1. app.config.from_object(settings)
        2. app.config.from_pyfile('settings.py')
```
### 1.2.5 启动：
```
    manager.run()  ---->启动
    使用命令在终端：python3 app.py runserver -h 0.0.0.0 -p 5001
    
    扩展：manager自定义添加命令：
    @manager.command
    def init():
        print('初始化')
    
    python3 app.py init
```

# 二、flask路由和请求响应对象
## 2.1、路由定义
路由和请求request，响应response
flask是基于Werkzeug工具包的一个web服务框架，所以flask里视图函数的实现，实际上是对werkzeug的一层封装

路由结合视图函数
    @app.route('/')
    def hello_world():  # ---->视图函数
        return 'HELLO hello world!hello kitty!'
```
        def route(self, rule, **options):
        def decorator(f):
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator
        这个装饰器其实就是将rule字符串跟视图函数进行了绑定，通过add_url_rule()实现的绑定
        @app.route('/index')
        def index():
            return 'welcome everyone！'
        
        等效的
        def index():
            return 'welcome everyone！'
        app.add_url_rule('/index', view_func=index)
```

## 2.2、路径（路由）的变量规则：
### 2.2.1 转换器：
         str 默认
         int  整型
         float 浮点型
         path  类似str，但是可以识别'/'
         uuid  识别uuid类型的字符串

   @app.route('/news/<int:num>')   ----><int:num>表示的就是一个变量
```
    @app.route('/getcity/<key>')  # key就是一个变量名，默认是字符串类型的
    def get_city(key):  # 参数是必须添加的
        print(type(key))
        return data.get(key)
```
### 2.2.2 反向解析（通过endpoint找url）
```
（1）概念：
		获取请求资源路径
（2）语法格式：
		url_for(蓝图的名字.方法名字)
（3）使用：
         @blue.route("/hehe/", methods=["GET","POST","PUT"])
          def hehe():
              return "呵呵哒"

          @blue.route("/gethehe/")
          def get_hehe():
              p = url_for("first.hehe")
          return p
```
```
@app.route('rule',endpoint='value')
def func():
    pass

url_for('value') 无endpoint即url_for('func')  -----------> 根据endpoint找到路由rule
```

### 2.2.3 视图函数
#### 2.2.3.1 请求:request
from flask import request
  client 发出的请求

request对象   只要有请求则会产生一个request对象
```
属性：
    request.method  获取请求的方式
    request.args.get('key',默认值)    ----> 一般用于get方式，请求参数中获取
        # 例如：/register2?username=zhangsan&address=Beijing
    request.form.get('key',默认值)    ----> 一般用于post方式，请求体中获取
        # 注意post提交必须在路由中进行设置，通过methods = ['GET','POST']
    request.header.get('key',默认值)     ----> 请求头中获取
    request.cookie.get('key',默认值)     ----> cookie中获取
    request.file.get('key',默认值)       ----> 获取文件对象

    request.values ----> [dictA,dictB]  dictA---GET   dictB--POST
    request.get_json()  application/json 类型数据
    request.get_data()  将数据构成一个字节字符串
    
    request.remote_addr  获取远程的ip地址
    print(request.path)  # /  (路由中的路径)
    print(request.full_path)  # /?name=admin
    print(request.url)  # http://127.0.0.1:5000/?name=admin
    print(request.base_url)  # http://127.0.0.1:5000/
    print(request.url_root)
    print(request.query_string)  # b'name=admin'
    host_url    （只有主机和端口号的url）	
```

#### 2.2.3.2 响应:response
返回值：其实返回值返回的都是一个响应对象，response响应对象。
```
    print(response.content_type)
    print(response.headers)
    print(response.status_code)  # 200
    print(response.status)  # 200 OK
```
- 重要
```
    在视图函数的返回值后面可以跟：
    1.string   系统会自动将str转成一个response对象。# 还有第二个返回，放的是状态码(return '德玛西亚',404)
    2.dict    使用jsonify函数将其转换为json格式字符串，作为response对象的请求体
    3.response对象。res = Response('成功')
    4.make_reponse( ) 构建response对象，可以给response对象添加一些头部信息。（resp = make_response('<h2>xxxxxxxx</h2>',502)）
    5.jsonify(datas)  将datas转成json的格式  dict默认使用此函数
    6.render_template() 模板渲染,将模板变成字符串。（resp = render_template('Response.html')）
    7.redirect() 重定向  302状态码。（return redirect('/makeresponse/')）
    8.tuple
```

### 2.2.4 异常
```
abort
	直接抛出 显示错误状态码  终止程序运行
	abort(404)
	eg:
		@blue.route('/makeabort/')
         def make_abort():
              abort(404)
              return '天还行'

捕获
	@blue.errorhandler()
		- 异常捕获
		- 可以根据状态或 Exception进行捕获
		- 函数中要包含一个参数，参数用来接收异常信息
	eg:
	@blue.errorhandler(502)
    def handler502(exception):
        return '不能让你看到状态码'
```

### 2.2.5 模板
```
    如果想在视图函数中获取模板xxx.html的内容则通过render_template()
    render_template('模板名称') 返回值是一个字符串
    主要是通过模板引擎将模板内容转成字符串的形式。

    @app.route('/register')
    def register():
        return render_template('register.html')
```
    
### 2.2.6 蓝图
```
    from flask import Blueprint, url_for
    user_bp = Blueprint('user', __name__)

    @user_bp.route('/')
    def user_center():
        print(url_for('user.register'))  # 反向解析
        return '用户中心'
 
    @user_bp.route('/register')
    def register():
        return '用户注册'
```

# 三、flask模板语法

模板：（网页）
模板的语法：
## 3.1. 在模板中获取view中传递的变量值：{{ 变量名key }}
render_template('模板名字',**context)

render_template('模板名字',key=value,key=value)
```
传入模板变量类型：
    name = '沈凯'  # str
    age = 18  # int
    friends = ['建义', '陈璟', '小岳岳', '郭麒麟']  # list
    dict1 = {'gift': '大手镯', 'gift1': '鲜花', 'gift2': '费列罗'}  # dict
    # 创建对象
    girlfriend = Girl('美美', '安徽阜阳')  # 自定义的类构建的类型：Girl对象

模板中获取变量数据：
    {{ list.0 }}  同 {{ list[0] }}
    {{ dict.key }} 同 {{ dict.get(key) }}
    {{ girl.name }} 同 {{ 对象.属性 }}
```


 ## 3.2.  控制快:
 ```
    {{ 变量 }}

    {% if  条件 %}
    {% endif %}
    
    {% if  条件 %}
     条件为True
    {% else %}
     条件为False
    {% endif %}
        
    {% if 条件 %}
        pass
    {% elif 条件 %}
        pass
     ....
    {% endif %}

    {% for 变量 in 可迭代的对象 %}
        for循环要做的任务，如：{{ loop.index }}
    {% endfor %}
    
    可以使用loop变量
    loop.index  序号从1开始
    loop.index0  序号从0开始
    
    loop.revindex  reverse  序号是倒着的
    loop.revindex0
    
    loop.first 布尔类型   是否是第一行
    loop.last  布尔类型   是否是最后一行
    
    dict<users列表，列表中每个元素都是一个字典>:
    {% for v in users.0.values() %}   ---->获取值
        <p>{{ v }}</p>
    {% endfor %}
    
    {% for k in users.0.keys() %}   ----》获取键
        <p>{{ k }}</p>
    {% endfor %}
    
    {% for k,v in users.0.items() %}  ---》获取键值
        <p>{{ k }}---{{ v }}</p>
    {% endfor %}
```
## 3.3 过滤器
过滤器的本质就是函数 <通过管道`|`将数据传递给过滤器函数处理后再返回对应值>
模板语法中过滤器：
{{ 变量名 | 过滤器(*args) }}
{{ 变量名 | 过滤器 }}
```
常见的过滤器：
    1、 safe ： 禁用转译
    msg = '<h1>520快乐！</h1>'
    return render_template('show_2.html', girls=girls, users=users, msg=msg)
    不想让其转译：
    {{ msg | safe }}
    2、 capitalize：单词的首字母大写
    {{ n1 | capitalize }}
    3、lower和upper
    大小写的转换
    4、title 一句话中每个单词的首字母大写
     msg = 'She is a beautiful girl'
     {{ msg | title}}
    5、reverse  翻转
    {{ n1 | reverse}}
    6、format
    {{ '%s is %d years old' | format('lily',18) }}
    7、truncate 字符串截断

    list的操作：
    {# 列表过滤器的使用 #}
    {{ girls | first }}<br>
    {{ girls | last }}<br>
    {{ girls | length }}<br>
    {#{{ girls | sum }} 整型的计算 #}
    {{ [1,3,5,7,9] | sum }}<br>
    {{ [1,8,5,7,3] | sort }}<br>
```
## 3.4 自定义过滤器
```
过滤器本质就是函数
    1. 通过flask模块中的add_template_filter方法
        a. 定义函数，带有参数和返回值
        b. 添加过滤器  app.add_template_filter(function,name='')
        c. 在模板中使用： {{ 变量 | 自定义过滤器 }}
    2。使用装饰器完成
        a. 定义函数，带有参数和返回值
        b. 通过装饰器完成，@app.template_filter('过滤器名字')装饰步骤一的函数
        c. 在模板中使用： {{ 变量 | 自定义过滤器 }}
```
## 3.5 模板复用/继承
```
    需要模版继承的情况：
    1。 多个模板具有完全相同的顶部和底部
    2。 多个模板具有相同的模板内容，但是内容中部分不一样
    3。 多个模板具有完全相同的模板内容
    
    标签：
    {% block 名字 %}
    
    {% endblock %}
    
    1.定义父模板
    2.子模板继承父模板
    步骤：
    父模板：
    1。 定义一个base.html的模板
    2。 分析模板中哪些是变化的比如：{% block title %}父模板的title{% endblock %}
        对变化的部分用block进行"预留位置"也称作：挖坑
    3。注意：样式和脚本 需要提前预留
        {% block mycss %}{% endblock %}
        {% block myjs %}{% endblock %}
    
    子使用父模板：
    1。 {% extends '父模板的名称' %}将父模板继承过来
    2。 找到对应的block（坑）填充，每一个block都是有名字的。
```
## 3.6 include和宏<了解即可>
```
    include: 包含
    在A，B，C页面都共同的部分，但是其他页面没有这部分。
    这个时候考虑使用include
    步骤：
        1。先定义一个公共的模板部分,xxx.html
        2。谁使用则include过来， {% include '文件夹/xxx.html' %}
    
    
    宏：macro
    1。把它看作是jinja2的一个函数，这个函数可以返回一个HTML字符串
    2。目的：代码可以复用，避免代码冗余
    定义两种方式：
        1。在模板中直接定义：
            类似： macro1.html  中定义方式
        2。将所有宏提取到一个模板中：macro.html
           谁想使用谁导入：
           {% import 'macro.html' as xxx %}
           {{ xxx.宏名字(参数) }}
```
## 3.7 总结
```
    变量： {{ 变量 }}
    块：
    {% if 条件 %} ....{% endif %}
    {% for 条件 %} ....{% endfor %}
    {% block 条件 %} ....{% endblock %}
    {% macro 条件 %} ....{% endmacro %}
    
    {% include '' %}  包含
    {% import '' %}    导入宏
    {% extends '' %}
    
    {{ url_for('static',filename='') }}
    {{ hongname(xxx) }}
    
    view:
    @app.route('/',endpoint='',methods=['GET','POST'])
    def index():
        直接使用request
        return response|''|render_template('xxx.html')
    
    template:
      模板的语法
```
# 四、flask模型
```
    mtv概念：
        model  模型  ----》数据库
        template 模板
        view  视图

    安装：
        pip3 install pymysql        建公路
        pip3 install flask-sqlalchemy    实现ORM映射
        pip3 install flask-migrate     发布命令工具
```

## 4.1、配置数据库的连接路径
```
    mysql+pymysql://user:password@hostip:port/databasename
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flaskday05'
```
## 4.2、创建包ext
```
   __init__.py中添加：
   db = SQLAlchemy()   ---->必须跟app联系
   def create_app():
        ....
        db.init_app(app)
        return app
```
## 4.3、migrate:
```
    migrate = Migrate(app=app, db=db)
    manager.add_command('db', MigrateCommand)
```
## 4.4、创建模型：
```
    models.py：模型就是类，经常称作模型类

    class User(db.Model):      ------> user表
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        username = db.Column(db.String(15), nullable=False)
        password = db.Column(db.String(12), nullable=False)
        phone = db.Column(db.String(11), unique=True)
        rdatetime = db.Column(db.DateTime, default=datetime.now)

    常见的数据类型：
        Integer        整型
        String(size)   字符串类型，务必指定大小
        Text          长文本类型
        DateTime       日期时间
        Float         浮点类型
        Boolean        布尔类型
        PickleType     存储pickle类型  主要跟序列化有关
        LargeBinary    存储大的二进制类型
    
    可选的：
        primary_key=True   主键
        autoincrement=True  自增
        nullable=False      不允许为空
        unique=True         唯一
        default=datetime.now  默认值  可以设置成当前系统时间或者其他的值
```

## 4.5、使用命令：
```
    a. ************敲黑板（没导入则执行migrate无效）***************
       在app.py 中导入模型:from apps.user.models import User

    b. 在终端使用命令：db
        python3 app.py db init   -----》 产生一个文件夹migrations
        python3 app.py db migrate -----> 自动产生了一个版本文件
         项目
          | ---apps
          | ---ext
          | ---migrations    python3 app.py db init     只需要init一次
                   |---versions   版本文件夹
                        |---71edde7ee937_.py    ---》  python3 app.py db migrate  迁移
                        |---cc0dca61130f_.py
        python3 app.py db upgrade 同步
        python3 app.py db downgrade 降级
```

## 4.6、添加数据：以注册为例
```
    # 模板，视图与模型结合
    
    1. 找到模型类并创建对象
    user = User()
    2. 给对象的属性赋值
    user.username = username
    user.password = password
    user.phone = phone
    # 添加
    3.将user对象添加到session中（类似缓存）
    db.session.add(user)
    4.提交数据
    db.session.commit()
```

# 五、flask数据库操作
## 5.1 查询：
```
    查询所有： 模型类.query.all()    ~  select * from user;
    如果有条件的查询(一般用filter功能更强大，而不是filter_by)：
        模型类.query.filter_by(字段名 = 值)   ～  select * from user where 字段=值；
        模型类.query.filter_by(字段名 = 值).first()   ～  select * from user where 字段=值 limit..；
        
        select * from user where age>17 and gender='男'；
        select * from user where username like 'zhang%';
        select * from user where rdatetime> xxx and rdatetime < xxx;
    
    模型类.query.filter()  里面是布尔的条件   模型类.query.filter(模型名.字段名 == 值)
    模型类.query.filter_by()  里面是一个等值   模型类.query.filter_by(字段名 = 值)
```

- ***** 模型类.query.filter() ******
```
    1. 模型类.query.filter().all()   -----> 列表
    2. 模型类.query.filter().first()  ----->对象-从列表中取出第一条数据
    3.User.query.filter(User.username.endswith('z')).all()   select * from user where username like '%z';
      User.query.filter(User.username.startswith('z')).all()  # select * from user where username like 'z%';
      User.query.filter(User.username.contains('z')).all()  # select * from user where username like '%z%';
      User.query.filter(User.username.like('z%')).all()
    
    多条件：
        from sqlalchemy import or_, and_,not_
        并且： and_    或： or_   非： not_
        User.query.filter(or_(User.username.like('z%'), User.username.contains('i'))).all()
        类似： select * from user where username like 'z%' or username like '%i%';
        
        User.query.filter(and_(User.username.contains('i'), User.rdatetime.__gt__('2020-05-25 10:30:00'))).all()
        # select * from user where username like '%i%' and rdatetime < 'xxxx'
        
        补充：__gt__,__lt__,__ge__(gt equal),__le__ （le equal）  ----》通常应用在范围（整型，日期）
        也可以直接使用 >  <  >=  <=  !=
        
        User.query.filter(not_(User.username.contains('i'))).all()
        
        18 19 20 17 21 22 ....
        select * from user where age in [17,18,20,22];
        User.username.in_(['','',''])
    
    排序：order_by
        user_list = User.query.filter(User.username.contains('z')).order_by(-User.rdatetime).all()  # 先筛选再排序
        user_list = User.query.order_by(-User.id).all()  对所有的进行排序
        注意：order_by(参数)：
        1。 直接是字符串： '字段名'  但是不能倒序
        2。 填字段名： 模型.字段    order_by(-模型.字段)  倒序
    
    限制： limit
        # limit的使用 + offset
        # user_list = User.query.limit(2).all()   默认获取前两条
        user_list = User.query.offset(2).limit(2).all()   跳过2条记录再获取两条记录
```

## 5.2 查询总结：
```
    1. User.query.all()  所有-列表
    2. User.query.get(pk)  一个对象-根据主键获取
    3. User.query.filter()   *   ？？？？？？？
     如果要检索的字段是字符串（varchar，db.String）:
       User.username.startswith('')
       User.username.endswith('')
       User.username.contains('')
       User.username.like('')
       User.username.in_(['','',''])
       User.username == 'zzz'
    如果要检索的字段是整型或者日期类型：
       User.age.__lt__(18)
       User.rdatetime.__gt__('.....')
       User.age.__le__(18)
       User.age.__ge__(18)
       User.age.between(15,30)
    
     多个条件一起检索： and_, or_
     非的条件： not_
    
     排序：order_by()
     获取指定数量： limit() offset()
    4. User.query.filter_by()
```

## 5.3 删除:
```
    两种删除：
    1。逻辑删除（定义数据库中的表的时候，添加一个字段isdelete，通过此字段控制是否删除）
    id = request.args.get(id)
    user = User.query.get(id)
    user.isdelete = True
    db.session.commit()
    
    2。物理删除(彻底从数据库中删掉)
    id = request.args.get(id)
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
```

## 5.4 更新:
```
    id = request.args.get(id)
    user = User.query.get(id)
    # 修改对象的属性
    user.username= xxxx
    user.phone =xxxx
    # 提交更改
    db.session.commit()
```

# 六、flask模型关系和博客
```
    参考文档：模型-多表关系确认(外键-relationship).md
```

# 七、flask会话机制和验证码
## 7.1 原理：
```
1、cookie
    在网站中，HTTP请求是无状态的。也就是说，即使第一次用户访问服务器并登录成功后，第二次请求服务器依然不知道当前发起请求的是哪个用户。cookie的出现就是为了解决这个问题，第一次登录后服务器返回一些数据（cookie）给浏览器，浏览器将这些数据保存在本地。当用户发起第二次请求的时候，浏览器自动的将上次请求得到的cookie数据携带给服务器，服务器通过这些cookie数据就能分辨出当前发起请求的是哪个用户了。cookie存储的数据量有限，不同的浏览器有不同的存储大小，但一般不超过4K，因此使用cookie只能存储一些少量的数据。

2、session
    session与cookie的作用有点类似，都是为了存储用户相关的信息。不同的是，cookie是存储在本地浏览器，session存储在服务器。存储在服务器的数据会更加的安全，不容易被窃取。但存储在服务器也有一定的弊端，就是会占用服务器的资源。

3、cookie和session的结合使用
    web开发发展至今，cookie和session的使用已经出现了一些非常成熟的方案。在如今的市场和企业里，一般有两种存储方式：

    存储在服务器：通过cookie存储一个session_id，然后具体的数据则保存在session中。当用户已经登录时，会在浏览器的cookie中保存一个session_id，下次再次请求的时候，会把session_id携带上来，服务器根据session_id在session库中获取用户的session数据，从而能够辨别用户身份，以及得到之前保存的状态信息。这种专业术语叫做server side session
    将session数据加密，然后存储在cookie中。这种专业术语叫做client side session，flask采用的就是这种方式，但是也可以替换成其它形式
```

```
（1）cookie: 客户端浏览器的缓存；session: 服务端服务器的缓存
（2）cookie不是很安全，别人可以分析存放在本地的cookie并进行cookie欺骗，考虑到安全应当使用session
（3）session会在一定时间内保存在服务器上。当访问增多，会比较占用你服务器的性能，考虑到减轻服务器性能方面，应当使用cookie
可以考虑将登陆信息等重要信息存放为session，其他信息如果需要保留，可以放在cookie中
```

## 7.2 cookie方式：
```
Cookie
	1.客户端会话技术
	2.所有数据存储在客户端
	3.以key-value进行数据存储层
	4.服务器不做任何存储
	5.特性
		(1)支持过期时间
			max_age  毫秒
			expries  具体日期
		(2)根据域名进行cookie存储
		(3)不能跨网站（域名）
		(4)不能跨浏览器
		(5)自动携带本网站的所有cookie
	6.cookie是服务器操作客户端的数据
	7.通过Response进行操作

cookie登陆使用
	设置cookie     response.set_cookie('username',username)
	获取cookie     username = request.cookies.get('username','游客')
	删除cookie     response.delete_cookie('username')
```

```
  保存：
    通过response对象保存。
    response = redirect(xxx)
    response = render_template(xxx)
    response = Response()
    response = make_response()
    response = jsonify()
    # 通过对象调用方法
    response.set_cookie(key,value,max_age)
    其中max_age表示过期时间，单位是秒
    也可以使用expires设置过期时间，expires=datetime.now()+timedelta(hour=1)

  获取：
    通过request对象获取。
    request.form.get()
    request.args.get()
    cookie也在request对象中
    request.cookies.get(key) ----> value

  删除：
    通过response对象删除。 把浏览器中的key=value删除了
    response = redirect(xxx)
    response = render_template(xxx)
    response = Response()
    response = make_response()
    response = jsonify()
    # 通过对象调用方法
    response.delete_cookie(key)
```

## 7.3 session：  是在服务器端进行用户信息的保存。一个字典
```
Session
	1.服务端会话技术
	2.所有数据存储在服务器中
	3.默认存在服务器的内存中
		- django默认做了数据持久化（存在了数据库中）
	4.存储结构也是key-value形势，键值对
	【注】单纯的使用session是会报错的，需要使用在__init__方法中配置app.config['SECRET_KEY']=‘110’

session登陆使用
	设置    session['username'] = username
	获取    session.get('username')
	删除
		   resp.delete_cookie('session')
		   session.pop('username')
```

```
    注意：
        使用session必须要设置配置文件，在配置文件中添加SECRET_KEY='xxxxx'，
        添加SECRET_KEY的目的就是用于sessionid的加密。如果不设置会报错。

    设置：
        如果要使用session，需要直接导入：
        from flask import session
    
    把session当成字典使用，因此：session[key]=value
    就会将key=value保存到session的内存空间
    **** 并会在响应的时候自动在response中自动添加有一个cookie：session=加密后的id ****
    获取
        用户请求页面的时候就会携带上次保存在客户端浏览器的cookie值，其中包含session=加密后的id
        获取session值的话通过session直接获取，因为session是一个字典，就可以采用字典的方式获取即可。
        value = session[key] 或者 value = session.get(key)
        这个时候大家可能会考虑携带的cookie怎么用的？？？？
        其实是如果使用session获取内容,底层会自动获取cookie中的sessionid值，
        进行查找并找到对应的session空间
    
    删除
        session.clear()  删除session的内存空间和删除cookie
        del session[key]  只会删除session中的这个键值对，不会删除session空间和cookie
```

## 7.4 session持久化问题(了解即可)
- 持久化简介

  ```
  1.django中对session做了持久化，存储在数据库中
  2.flask中没有对默认session进行任何处理
      - flask-session 可以实现session的数据持久化
      - 可以持久化到各种位置，更推荐使用redis
      - 缓存在磁盘上的时候，管理磁盘文件使用lru, 最近最少使用原则
  ```

- 持久化实现方案
```
	1.pip install flask-session
			在国内源安装
			pip install flask-sessin -i https://pipy.douban.com/simple
	2.初始化Session对象 
			（1）持久化的位置
				配置init中app.config['SESSION_TYPE'] = 'redis'
				
			（2）初始化
				创建session的对象有2种方式 分别是以下两种
				1 Session(app=app)
				2 se = Session()   se.init_app(app = app)
				
			（3）安装redis   
				pip install redis
				设置了默认开机启动，如果没有设置，那么需要将redis服务开启
				
			 (4)需要配置SECRET_KEY='110'
			 	注意：flask把session的key存储在客户端的cookie中，通过这个key可以从flask的内存中获取					 用户的session信息，出于安全性考虑，使用secret_key进行加密处理。所以需要先设置secret_key的值。
			 	
			（5）其他配置--视情况而定
				app.config['SESSION_KEY_PREFIX']='flask'
		
     特殊说明：
            查看redis内容
                    redis-cli
                    keys *
                    get key
            session生存时间31天	
                ttl session
                    flask的session的生存时间是31天，django的session生存时间是14天
```

# 八、flask钩子+文件上传+分页
## 8.1 钩子
```
1.登录权限的验证
    只要走center路由，判断用户是否是登录状态，如果用户登录了，可以正常显示页面，如果用户没有登录
    则自动跳转到登录页面进行登录，登录之后才可以进行查看。
    
    钩子函数：
    直接应用在app上：
    before_first_request
    before_request
    after_request
    teardown_request
    
    应用到蓝图：
    before_app_first_request
    before_app_request
    after_app_request
    teardown_app_request
```

## 8.2 文件上传
```
 A. 本地上传
    注意：
    表单：  enctype="multipart/form-data"
 <form action="提交的路径" method="post" enctype="multipart/form-data">
        <input type="file" name="photo" class="form-control">
        <input type="submit" value="上传相册" class="btn btn-default">
 </form>
   view视图函数：
   photo = request.files.get('photo')   ----》photo是FileStorage

   属性和方法：FileStorage = 》fs
   fs.filename
   fs.save(path)  ----> path上传的路径os.path.join(UPLOAD_DIR,filename)
   fs.read()  ----> 将上传的内容转成二进制方式

 B. 上传到云端（对象存储）
    本地的资源有限或者是空间是有限的
    https://developer.qiniu.com/kodo/sdk/1242/python  ---》参照python SDK

    util.py:
    def upload_qiniu():
        #需要填写你的 Access Key 和 Secret Key
        access_key = 'Access_Key'
        secret_key = 'Secret_Key'
        #构建鉴权对象
        q = Auth(access_key, secret_key)
        #要上传的空间
        bucket_name = 'Bucket_Name'
        #上传后保存的文件名
        key = 'my-python-logo.png'
        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)
        #要上传文件的本地路径
        localfile = './sync/bbb.jpg'
        ret, info = put_file(token, key, localfile)
        print(info)

        ---->put_data()  适用于从filestorage里面读取数据实现上传
        ---->put_file()  指定文件路径上传

    def delete_qiniu():
        pass
```
## 8.3 分页
```
评论：
    文章的详情：必须携带aid，aid表示的是文章的主键id
    通过主键id得到文章对象
    如果还有其他内容的分页，就需要在路由携带page
    例如：http://127.0.0.1:5000/article/detail?page=2&aid=1

分页：
    print(pagination.items)  # [<Article 4>, <Article 3>, <Article 2>]
    print(pagination.page)  # 当前的页码数
    print(pagination.prev_num)  # 当前页的前一个页码数
    print(pagination.next_num)  # 当前页的后一页的页码数
    print(pagination.has_next)  # True
    print(pagination.has_prev)  # True
    print(pagination.pages)  # 总共有几页
    print(pagination.total)  # 总的记录条数
```

# 九、flask使用redis缓存
## 9.1 准备：
```
    pip install redis
    pip install flask-caching

    启动redis
    进到redis目录：
       redis-server redis.windows.conf
```
## 9.2 使用缓存：
```
    1. Cache对象
       from flask-caching import Cache
       cache = Cache()

    2.
    config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': '127.0.0.1',
        'CACHE_REDIS_PORT': 6379
    }

    def create_app():
        .....
        cache.init_app(app,config)

    3. 设置缓存:
       cache.set(key,value,timeout=second)   ----> flask_cache_pic_abc
       cache.set_many([(key,value),(key,value),(key,value),...])

       获取缓存值:
       cache.get(key)  --->value
       cache.get_many(key1,key2,...)

       删除缓存:
       cache.delete(key)
       cache.delete_many(key1,key2,...)
       cache.clear()

    视图函数缓存<即缓存网页，使得网页加载更快，比如下面缓存index首页>:
    @app.route("/")
    @cache.cached(timeout=50)
    def index():
        return render_template('index.html')
```
## 9.3 案例：
```
SMS: 手机短信验证码登录
1. 获取验证码：
   1.1. 输入手机号码
   1.2. 通过ajax发送请求
   1.3. 后端： 获取手机号码
      使用requests向第三方的服务端（网易云信）发送请求
      URL https://api.netease.im/sms/sendcode.action
      method： POST
      header:
        headers={}
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        AppSecret = 'ee8d51d1061e'
        Nonce = '74093849032804'
        CurTime = str(time.time())
        headers['AppKey'] = 'cc735ffe22684cc4dab2dc943540777c'
        headers['Nonce'] = Nonce
        headers['CurTime'] = CurTime
        s = AppSecret + Nonce + CurTime
        headers['CheckSum'] = hashlib.sha1(s.encode('utf-8')).hexdigest().lower()
        res = requests.post(url, data={'mobile': phone}, headers=headers)
    1.4.获取响应对象：
       res.text     文本内容
       res.content  二进制

    1.5. 转成json对象
       r = json.loads(res.text)

       r.obj  ---> 验证码

       保存到缓存中: cache.set(phone,r.obj)

    1.6. 返回json结果给ajax

2.登录验证：
   获取手机号码和验证码进行验证
        phone = request.form.get('phone')
        validate = request.form.get('valiadate')
        code = cache.get(phone)
        if code == validate:
            user = User.query.filter(User.phone == phone).first()
            cache.set('uname', user.username)
            session['uname'] = user.username
            return redirect(url_for('blog.index'))
        else:
            flash('手机验证码错误')
            return render_template('login_phonecode.html')
```
# 十、绘制图片验证码（了解即可）
```
1、封装绘制图片验证码的函数
# 如果是前后端分离的场景，一般后端只需要返回json字符串code，前端拿到code后再绘制图片验证码
util.py：
    import random
    from PIL import Image, ImageFont, ImageDraw, ImageFilter
    
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def generate_image(length):
        s = 'qwerQWERTYUIOtyuiopas123456dfghjklPASDFGHJKLZXCVBNMxcvbnm7890'
        size = (130, 50)
        # 创建画布
        im = Image.new('RGB', size, color=get_random_color())
        # 创建字体
        font = ImageFont.truetype('font/方正正中黑简体.ttf', size=35)
        # 创建ImageDraw对象
        draw = ImageDraw.Draw(im)
        # 绘制验证码
        code = ''
        for i in range(length):
            c = random.choice(s)
            code += c
            draw.text((5 + random.randint(4, 7) + 25 * i, 1),
                      text=c,
                      fill=get_random_color(),
                      font=font)
        # 绘制干扰线
        for i in range(8):
            x1 = random.randint(0, 130)
            y1 = random.randint(0, 50 / 2)
    
            x2 = random.randint(0, 130)
            y2 = random.randint(50 / 2, 50)
    
            draw.line(((x1, y1), (x2, y2)), fill=get_random_color())
    
        im = im.filter(ImageFilter.EDGE_ENHANCE)
        return im, code
    
    if __name__ == '__main__':
        generate_image(4)

2、接口视图函数调用
    from io import BytesIO
    
    @app.route('/image')
    def get_image():
        im, code = generate_image(4)
        # 将image对象转成二进制
        buffer = BytesIO()
        im.save(buffer, "JPEG")
        buf_bytes = buffer.getvalue()
        # 保存到session中
        session['valid'] = code
        response = make_response(buf_bytes)
        response.headers['Content-Type'] = 'image/jpg'
        return response
```
# 十一、flask_bootstrap、flask_wtf（了解即可）
```
flask_bootstrap（对wtform模块做的封装）：
    1、没使用flask封装的bootstrap模块，因为封装的可能是bootstrap3，而我们想使用最新的bootstrap5
    2、使用封装的flask_bootstrap模块，需要学习下此模块的一些语法，没必要，直接使用原生的bootstrap设计页面即可
flask_wtf：
    1、flask_wtf集成了wtform，csrf的保护和文件上传功能，图形验证码。可以对表单提交内容进行验证。
    2、没使用此模块，因为后面前后端分离场景下，restful-api的请求参数验证对象有对提交内容做验证的功能<包括正则表达式>
    3、其次，使用flask_wtf模块也需要学习下此模块的用法，麻烦。并且此模块自动生成的表单不好单独控制css样式。

flask_wtf使用：
    1、安装：
    pip3 install Flask-WTF
    
    全局使用csrf保护，
    csrf = CSRFProtect(app=app)
    必须需要设置SECRET_KEY这个配置项
    app.config['SECRET_KEY'] = 'fgfhdf4564'
    
    2、定义form.py:
    在文件中中添加：
    class UserForm(FlaskForm):
        name = StringField('name', validators=[DataRequired()])
    
    各种：Field类型
    StringField
    PasswordField
    IntegerField
    DecimalField
    FloatField
    BooleanField
    RadioField
    SelectField
    DatetimeField
    
    各种的验证：
    DataRequired
    EqualTo
    IPAddress
    Length
    NumberRange
    URL
    Email
    Regexp
    
    3、使用：
     视图中：
       .....
       form =UserForm()
       return render_template('user.html',form=form)
    
     模板中：
        <form action='' method=''>
          {{form.csrf_token}}
          {{form.name}}
          {{form.password}}
          <input type='submit' value=''/>
        </form>
    
    4、提交验证：
    @app.route('/',methods=['GET','POST'])
    def hello_world():
        uform = UserForm()
        if uform.validate_on_submit():   ------->主要通过validate_on_submit进行校验
            print(uform.name)
            print(uform.password)
            return '提交成功！'
        return render_template('user.html', uform=uform)

flask_wtf文件上传：
    1、定义form
    class UserForm(FlaskForm):
        。。。。。。
        # 上传使用的就是FileField，如果需要指定上传文件的类型需要使用：FileAllowed
        icon = FileField(label='用户头像', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], message='必须是图片文件格式')])
    
    2、模板中的使用同其他类型的字段，但是必须在form上面：enctype="multipart/form-data"
    
    3、视图函数中如果验证成功，通过：
            icon = uform.icon.data   -----》icon是FileStorage类型
            filename = secure_filename(icon.filename)
            icon.save(os.path.join(UPLOAD_DIR, filename))
```
# 十二、flash消息闪现（了解即可）
```
1. 闪现：
    记住：
    1、在一个请求结束的时候<即视图函数return前>添加flash
        flash('恭喜！验证成功啦！','info')
        flash('哈哈哈','error')
        flash(username,'warning')
    2、在当前请求中渲染获取或者仅仅下一个请求中可以获取。

    添加闪现：（后面的类型是可选择的）
    flash('恭喜！验证成功啦！','info')
    flash('哈哈哈','error')
    flash(username,'warning')

    获取闪现内容：
    get_flash_messages(with_categories=[True/False])
    get_flashed_messages(category_filter=["error"])  可选的
    有针对性的获取对应类型的闪现消息

2、案例（html模板中获取闪现的消息）：
    {% with messages = get_flashed_messages(with_categories=True) %}
        {% if messages %}
            <ul>
                {% for category, message in messages %}
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    <a href="{{ url_for('test') }}">测试下一次请求中闪现数据能否获取</a>
```

# 十三、logger日志
```
用uwsgi方式启动flask默认会将日志输出到uwsgi.log中，当然我们也可以自定义日志格式并输出到其他文件中
uwsgi ----》 uwsgi.log

logger：
    1.使用app自带，
        app.logger.info('')
        app.logger.debug('A value for debugging')
        app.logger.warning('A warning occurred (%d apples)', 42)
        app.logger.error('An error occurred')

    2.通过logging进行创建：
        import logging
        logger = logging.getLogger('name')  # 默认flask的logger的名字叫：app
        logger = logging.getLogger('app') # 创建时指定名为app，那么配置才对app的logger生效

    3.保存到文件：
    logger = logging.getLogger('app')
    # basicConfig配置基本属性，如果下面的配置有相同的会把基本属性覆盖了
    logging.basicConfig(filename='log.txt', filemode='a', level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("log1.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    4.使用logger.info('message')
```

# 十四、flask_restful（**重要，前后端分离）
## 14.1 基本概念
```
什么是RESTful架构：
    （1）每一个URI代表一种资源；
    （2）客户端和服务器之间，传递这种资源的某种表现层；
    （3）客户端通过四个HTTP动词(GET,POST,PUT,DELETE,[PATCH])，对服务器端资源进行操作，实现"表现层状态转化"。
        # 后端接口一般用Postman调用测试

前后端分离：
    前端：app，小程序，pc页面
    后端：没有页面，mtv： 模型模板视图  去掉了t模板。
        mv：模型 视图
        模型的使用：跟原来的用法相同
        视图： api构建视图

restful后端基本使用步骤：
     1. pip3 install flask-restful
    
     2.创建api对象
      api = Api(app=app)
      api = Api(app=蓝图对象)
        案例：蓝图与api使用
        user_bp = Blueprint('user', __name__)
        api = Api(user_bp)
        class xxxxApi(Resource):
            pass
        api.add_resource(xxxxApi,'/xxxx')
     3.定义类视图：
      from flask_restful import Resource
      class xxxApi(Resource):
        def get(self):
            pass
    
        def post(self):
            pass
    
        def put(self):
            pass
    
        def delete(self):
            pass
      4. 绑定
      api.add_resource(xxxApi,'/user')

参照：http://www.pythondoc.com/Flask-RESTful/quickstart.html
https://flask-restful.readthedocs.io/en/latest/

restful路由和route路由区别：
    route：
        @app.route('/user')
        def user():              -------》视图函数
            .....
            return response对象
    
        增加  修改   删除   查询  按钮动作
        http://127.0.0.1:5000/user?id=1&*=*   -->增加/查询
        http://127.0.0.1:5000/userdel?id=1    -->删除
        http://127.0.0.1:5000/userchange?id=1 -->修改

    restful：
        # restful（后面几个术语概念基本相同）: ---->api ----> 接口 ---->资源 ----> url
        class xxx（Resource）：  -------> 类视图
            def get(self):
                pass
            ....
        
        http://127.0.0.1:5000/user
        get、post、put、delete
        增加  修改   删除   查询  是通过请求方式完成的
        # 如：http://127.0.0.1:5000/goods?type=xxx&page=1&sorted=price   ----》get

        路径产生:
        api.add_resource(Resource的子类，'/user')
        api.add_resource(Resource的子类，'/goods')
        api.add_resource(Resource的子类，'/order')
```
## 14.2 flask_restful进：请求参数传入
```
步骤：
1。创建RequestParser对象：
    # 参数解析
    parser = reqparse.RequestParser(bundle_errors=True)  # 解析对象
2。给解析器添加参数：
    通过parser.add_argument('名字'，type=类型，required=是否必须填写，help=错误的提示信息，location=表明获取的位置form就是post表单提交)
    注意在type的位置可以添加一些正则的验证等。
    例如：
    parser.add_argument('username', type=str, required=True, help='必须输入用户名', location=['form'])
    parser.add_argument('password', type=inputs.regex(r'^\d{6,12}$'), required=True, help='必须输入6~12位数字密码',
                        location=['form'])
    parser.add_argument('phone', type=inputs.regex(r'^1[356789]\d{9}$'), location=['form'], help='手机号码格式错误')
    parser.add_argument('hobby', action='append')  # ['篮球', '游戏', '旅游']
    parser.add_argument('icon', type=FileStorage, location=['files'])
    只要添加上面的内容，就可以控制客户端的提交，以及提交的格式。
3。在请求的类视图函数中获取数据<获取数据时就会判断参数以及格式是否正确，不正确直接返回报错json>：
    可以在get，post，put等中获取数据，通过parser对象.parse_args()
    # 获取数据
    args = parser.parse_args()
    args是一个字典底层的结构中，因此我们获取具体的数据时可以通过get
    username = args.get('username')
    password = args.get('password')
```
## 14.3 flask_restful出：转json格式输出
### 14.3.1 出:marchal或marchal_with序列化
```
1、出：return data
    注意：data必须是符合json格式
    {
      'aa':10,
      'bb':[
         {
           'id':1,
           'xxxs':[
                    {},{}
                  ]
         },
         {
    
         }
      ]
    }
    如果直接返回不能有自定义的对象User，Friend，。。。。
    
2、如果接口返回的数据结构中包含自定义对象<如db表对象>，则需要定义对象的json序列化格式字典。如果有这种对象，需要：marchal(),marchal_with()帮助进行转换。
    1。marchal(对象，对象的fields格式)  # 对象的fields格式是指字典的输出格式
       marchal([对象，对象]，对象的fields格式)
    
    2。marchal_with() 作为装饰器修饰请求方法
        class UserFriendResource(Resource):
            @marshal_with(user_friend_fields)
            def get(self, id):
                friends = Friend.query.filter(Friend.uid == id).all()
                user = User.query.get(id)
        
                friend_list = []
                for friend in friends:
                    u = User.query.get(friend.fid)
                    friend_list.append(u)
        
                data = {
                    'username': user.username,
                    'nums': len(friends),
                    'friends': friend_list  # [user,user,user]
                    # 上面用的是marshal_with，还可用marchal方式，如：'friends': marchal(friend_list, user_fields)
                }
                return data
        # 函数需要参数user_friend_fields，参数就是最终数据输出的格式

        参数： user_friend_fields，类型是：dict类型
        例如：
        user_friend_fields = {
            'username': fields.String,
            'nums': fields.Integer,
            'friends': fields.List(fields.Nested(user_fields)) # Nested表示对列表中的每个对象用格式user_fields来做序列化
        }

        fields.Nested(fields.String)  ----> ['aaa','bbb','bbbc']
        fields.Nested(user_fields)  -----> user_fields是一个字典结构，将里面的每一个对象转成user_fields

3、总结
    当接口返回的数据结构比较复杂时<有列表/字典嵌套结构>建议用marchal、反之不复杂<无嵌套结构>则建议用marshal_with

参考面试题：https://www.cnblogs.com/Utopia-Clint/p/10824238.html
```
### 14.3.1 出:序列化格式中value数据的处理
```
1、直接将db对象的字段数据取出来序列化
    需要定义字典，字典的格式就是给客户端看的格式
    user_fields = {
        'id': fields.Integer,
        'username': fields.String(default='匿名'),
        'pwd': fields.String(attribute='password'),
        'udatetime': fields.DateTime(dt_format='rfc822')
    }
    
    客户端能看到的是： id，username，pwd，udatetime这四个key
    默认key的名字是跟model中的模型属性名一致，如果不想让前端看到命名，则可以修改
    但是必须结合attribute='模型的字段名'

2、将db对象的字段数据取出来做二次处理后再序列化（需要额外自定义fields）
    自定义fields
    1。必须继承Raw
    2。重写方法：
       def format(self):
            return 结果
    
    class IsDelete(fields.Raw):
        def format(self, value):
            print('------------------>', value)
            return '删除' if value else '未删除'
    user_fields = {
        。。。
        'isDelete1': IsDelete(attribute='isdelete'),
        。。。
    }
    # 通过上面的处理可以实现，如果isdelete字段为1则输出删除，为0则输出未删除

3、不用db对象的字段数据来序列化，用URI来作为序列化的数据
    URI: xxxdict<返回json字典中某一个key的值为url> ----->点击具体的一个获取详情的url ------> 详情
    涉及endpoint的定义：
    api.add_resource(UserSimpleResource, '/user/<int:id>', endpoint='single_user')

    定义两个user_fields,
    1.用于获取用户数据结构的fields<接口1的序列化格式字典>：
    user_fields_1 = {
        'id': fields.Integer,
        'username': fields.String(default='匿名'),
        'uri': fields.Url('single_user', absolute=True)  ----》参数使用的就是endpoint的值
    }
    # endpoint single_user的接口为/user/<int:id>,接口需要传入id参数，因此上面序列化字典所序列化的db对象中需要有id字段，这样接口才能拿到id参数
    # 解释：'id': fields.Integer表示会去将要序列化db对象中拿取属性名为id的value

    2.具体用户信息展示的fields<展示详情-接口2的序列化格式字典>
    user_fields = {
        'id': fields.Integer,
        'username': fields.String(default='匿名'),
        'pwd': fields.String(attribute='password'),
        'isDelete': fields.Boolean(attribute='isdelete'),
        'isDelete1': IsDelete(attribute='isdelete'),
        'udatetime': fields.DateTime(dt_format='rfc822')
    }
```
# 十五、跨域处理
```
跨域问题来源于JavaScript的"同源策略"，即只有 协议+主机名+端口号 (如存在)相同，则允许相互访问。
也就是说JavaScript只能访问和操作自己域下的资源，不能访问和操作其他域下的资源。
跨域问题是针对JS和ajax的，html本身没有跨域问题。

跨域问题可以在前端处理<但是前端处理需要和后端配合一起处理>，也可以后端处理<建议后端处理>
后端：
法1：使用第三方扩展：flask-cors
    from flask_cors import CORS
    cors= CORS()
    
    与app进行绑定
    cors.init_app(app=app,supports_credentials=True)

法2：法1相当于第三方模块会自动给每一次response添加以下的header
    response = make_response()
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Access-Control-Allow-Methods']='GET,POST'
    response.headers['Access-Control-Allow-Headers']='x-request-with,Content-type'
    return response
```
# 十六、安全
```
在OAuth协议中，token是在输入了用户名和密码之后获取的，
利用这个token你可以拥有查看或者操作相应的资源的权限。
你有这些权限，是因为服务器知道你是谁（authentication）以后赋予你的，
所以token这个东西，其实就是你的一个“代表”，或者说完全能代表你的“通行证”。

登录处理，记录登录状态：cookie，session，cache（redis），token，JWT<安全系数逐级增加>
```

# 十七、nginx
```
nginx：
1。轻量级
2。并发能力强
3。高度模块化
4。负载均衡
5。反向代理
    https://www.cnblogs.com/taostaryu/p/10547132.html
官网：
    http://nginx.org/en/docs/
安装：
    https://www.sohu.com/a/330919812_120149005
安装可以参照的路径:
    http://nginx.org/en/linux_packages.html#Ubuntu

启动Nginx
	nginx 	[ -c  configpath]   默认配置目录：/etc/nginx/nginx.conf
信息查看
	nginx 	-v
	nginx	-V
查看进程：
	ps -ef |grep nginx
控制Nginx
	nginx -s signal
		stop 		快速关闭
		quit		优雅的关闭
		reload		重新加载配置

通过系统管理
	systemctl  status  nginx	查看nginx状态
	systemctl  start    nginx	启动nginx服务
	systemctl  stop     nginx   关闭nginx服务
	systemctl  enable nginx	设置开机自启
	systemctl  disable nginx	禁止开机自启
```
