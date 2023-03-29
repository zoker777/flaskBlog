import os
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from settings import Config
from . import user_bp
from flask import render_template, request, redirect, url_for, session, jsonify, g, current_app
from exts import db, cache
from apps.utils.sendmsg import SmsSendAPIDemo, send_verification_code
from apps.users.model import User, Photo, AboutMe, MessageBoard
from apps.article.model import Article_type, Article
from apps.utils.util import upload_qiniu, delete_qiniu


required_login_list = ['/user/center',
                       '/user/change',
                       '/article/publish',
                       '/user/upload_photo',
                       '/user/photo_del',
                       '/user/myphoto',
                       '/article/add_comment',
                       '/article/publish_article',
                       '/user/aboutme',
                       '/user/showabout']


# ****重点*****
# 注意：下面的钩子对整个app生效，而不是只对某个蓝图生效
@user_bp.before_app_request
def before_request():
    current_app.logger.info(f'before_app_request钩子函数正在处理路由: {request.path}')
    # print('before_request', request.path)
    types = Article_type.query.all()
    g.types = types
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.filter(and_(User.isdelete == 0, User.id == user_id)).first()
        g.user = user
    else:
        g.user = None

    # 筛选路由拦截
    if request.path in required_login_list:
        if not user_id:
            return render_template('user/login.html')
        # else:
        #     # user = User.query.get(user_id)
        #     # 要做登录验证的路由中，都需要判断session的user_id是否存在，并且拿到user对象传到html模板中，
        #     # 现在通过钩子函数+g对象，可以简化代码，每个路由中不用单独判断了，都交给钩子函数判断即可。
        #     user = User.query.filter(and_(User.isdelete == 0, User.id == user_id)).first()
        #     # g对象，本次请求的对象<类似于往对象里面添加属性，user属性等于user>
        #     g.user = user

# # 一般需要对返回的response对象做特殊处理才会用到此函数，很少用
# @user_bp.after_app_request
# def after_request_test(response):
#     response.set_cookie('a', 'bbbb', max_age=19)
#     return response

# 自定义过滤器
@user_bp.app_template_filter('cdecode1')
def content_decode1(content):
    content = content.decode('utf-8')
    return content

# 首页
@user_bp.route('/')
def index():
    # 获取文章列表   7 6 5  |  4 3 2 | 1
    # 接收页码数
    page = int(request.args.get('page', 1))
    # 下面"-"降序
    pagination = Article.query.order_by(-Article.pdatetime).paginate(page=page, per_page=3)
    # print(pagination.items)  # [<Article 4>, <Article 3>, <Article 2>]
    # print(pagination.page)  # 当前的页码数
    # print(pagination.prev_num)  # 当前页的前一个页码数
    # print(pagination.next_num)  # 当前页的后一页的页码数
    # print(pagination.has_next)  # True
    # print(pagination.has_prev)  # True
    # print(pagination.pages)  # 总共有几页
    # print(pagination.total)  # 总的记录条数

    # 下面注释的为没在钩子函数中添加获取user、types的代码
    # # 获取分类列表
    # types = Article_type.query.all()
    # # 判断用户是否登录
    # user_id = session.get('user_id', None)
    # user = User.query.filter(and_(User.isdelete == 0,User.id == user_id)).first()
    # if user:
    #     return render_template('user/index.html', user=user, types=types, pagination=pagination)
    # return render_template('user/index.html', types=types, pagination=pagination)
    return render_template('user/index.html', pagination=pagination)

@user_bp.route('/center')
def user_center():
    # 测试logger
    current_app.logger.info('用户正在访问用户中心页面')

    # 下面注释的为没在钩子函数中添加获取user、types的代码
    # types = Article_type.query.all()
    photos = Photo.query.filter(Photo.user_id == g.user.id).all()
    # return render_template('user/center.html', user=g.user, types=types, photos=photos)
    return render_template('user/center.html', photos=photos)

@user_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        users = User.query.filter(and_(User.isdelete == 0,User.phone == phone)).all()
        if users:
            msg = '用户手机号已注册'
            return render_template('user/register.html', msg=msg)
        new_user = User()
        new_user.username = username
        new_user.password = password
        new_user.phone = phone
        db.session.add(new_user)
        db.session.commit()
        print('注册成功')
        return redirect(url_for('user.login'))
    return render_template('user/register.html')

@user_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        f = request.args.get('f')
        if f == '1':  # 用户名登录
            username = request.form.get('username')
            password = str(request.form.get('password'))
            user = User.query.filter(
                and_(User.isdelete == 0, User.username == username, User.password == password)).first()
            if user:
                session['user_id'] = user.id
                return redirect(url_for('user.index'))
                # return render_template('user/index.html', user=user)
            return render_template('user/login.html', msg='用户or密码认证失败')
        elif f == '2':  # 验证码登录
            phone = request.form.get('phone')
            code = request.form.get('code')
            user = User.query.filter(
                and_(User.isdelete == 0, User.phone == phone)).first()
            if user:
                # 验证短信验证码
                # valid_code = session.get(phone, None) # 旧-session方式存储短信验证码
                valid_code = cache.get(phone)  # 新-redis方式存储短信验证码
                current_app.logger.info(f'valid_code={valid_code},code={code}')
                if valid_code == code:
                    session['user_id'] = user.id
                    return redirect(url_for('user.index'))
            return render_template('user/login.html', msg='手机号or验证码认证失败')
    return render_template('user/login.html')

@user_bp.route('/logout')
def logout():
    # del session['user_id'] # 一般不用这个
    # session.pop(key)：删除指定值、del session[key]：删除指定值、session.clear()：删除session中所有的值
    session.clear()
    return redirect(url_for('user.index'))

@user_bp.route('/sendMsg')
def send_message():
    phone = request.args.get('phone')
    # 验证手机号码是否注册，否则不发送验证码，节省成本
    user = User.query.filter(
        and_(User.isdelete == 0, User.phone == phone)).first()
    if not user:
        return jsonify(code=400, msg='手机号码未注册')
    # 发送验证码
    ret, code = send_verification_code(phone)
    print('验证码：=================================================>',code)
    if ret is not None:
        if ret["code"] == 2:
            smsId = ret["smsid"]
            # 假设存放的验证码都是959300，选择phone作为key，可以两次区分不同用户<session+phone>。其实session中phone换为一个固定key也行，不同用户session本就是隔离的。
            # session[phone]=code  # 旧-session方式存储短信验证码
            # 短信验证码可以用redis来存储。session对每个用户天然隔离的，因此用session存储，key名相同也没关系。但redis是大家共用的大池子，key名必须不同，用phone作为key即可。
            # 因为session不能单独对某个key设置timeout，因此采用redis来存储短信验证码，并为其设置3分钟的timeout
            cache.set(phone, code, timeout=180)  # 新-redis方式存储短信验证码
            return jsonify(code=200,msg='短信发送成功')
        else:
            print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
            return jsonify(code=400,msg='短信发送失败')
    return jsonify(code=400,msg='API接口调用失败')

# 手机号码验证
@user_bp.route('/checkphone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(and_(User.isdelete == 0, User.phone == phone)).first()
    # code: 400 不能用    200 可以用
    if user:
        return jsonify(code=400, msg='此号码已被注册')
    else:
        return jsonify(code=200, msg='此号码可用')

# 图片的扩展名
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

# 用户信息修改
@user_bp.route('/change', methods=['GET', 'POST'])
def user_change():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        # 只要有图片，获取方式必须使用request.files.get(name)
        icon = request.files.get('icon',None)
        # 属性： filename 用户获取文件的名字
        # 方法:  save(保存路径)
        user = g.user
        if icon:
            icon_name = icon.filename  # 1440w.jpg
            suffix = icon_name.rsplit('.')[-1]
            if suffix in ALLOWED_EXTENSIONS:
                icon_name = secure_filename(icon_name)  # 保证文件名是符合python的命名规则
                file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
                icon.save(file_path)
                path = 'upload/icon'
                user.icon = os.path.join(path, icon_name)
                # windows下用join拼接有问题，默认以\拼接
                if '/' in user.icon:
                    user.icon = user.icon.replace('\\', '/')
            else:
                return render_template('user/center.html', user=g.user, msg='扩展名格式必须为：jpg,png,gif,bmp格式')
        # 保存成功
        user.username = username
        user.phone = phone
        user.email = email
        db.session.commit()
        return redirect(url_for('user.user_center'))
        # 查询一下手机号码<修改手机号码时用了ajax判断手机号码是否存在，因此以下几行可以注释>
        # users = User.query.all()
        # for user in users:
        #     if user.phone == phone:
        #         # 说明数据库中已经有人注册此号码
        #         return render_template('user/center.html', user=g.user,msg='此号码已被注册')
    # return render_template('user/center.html', user=g.user)
    return render_template('user/center.html')

# 上传照片
@user_bp.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    # 获取上传的内容
    photo = request.files.get('photo')  # FileStorage
    # photo.filename,photo.save(path)
    # 工具模块中封装方法
    ret, info = upload_qiniu(photo)
    if info.status_code == 200:
        photo = Photo()
        photo.photo_name = ret['key']
        photo.user_id = g.user.id
        db.session.add(photo)
        db.session.commit()
        return '上传成功！'
    else:
        return '上传失败！'


# 删除相册图片
@user_bp.route('/photo_del')
def photo_del():
    pid = request.args.get('pid')
    photo = Photo.query.get(pid)
    filename = photo.photo_name
    # 封装好的一个删除七牛存储文件的函数
    info = delete_qiniu(filename)
    # 判断状态码
    if info.status_code == 200:
        # 删除数据库的内容
        db.session.delete(photo)
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        referer = request.headers.get('Referer', None)
        return render_template('500.html', err_msg='删除相册图片失败！', referer=referer)


# 我的相册 and_(User.isdelete == 0, User.username == username, User.password == password)
@user_bp.route('/myphoto')
def myphoto():
    page = int(request.args.get('page', 1))
    # 分页操作
    # photos = Photo.query.paginate(page=page, per_page=6)
    photos = Photo.query.filter(Photo.user_id == g.user.id).paginate(page=page, per_page=6)
    # return render_template('user/myphoto.html', photos=photos, types=g.types, user=g.user)
    return render_template('user/myphoto.html', photos=photos)

@user_bp.route('/error')
def test_error():
    # print(request.headers)
    # print(request.headers.get('Accept-Encoding'))
    referer = request.headers.get('Referer', None)
    return render_template('500.html', err_msg='有误', referer=referer)

# 关于用户介绍添加
@user_bp.route('/aboutme', methods=['GET', 'POST'])
def about_me():
    content = request.form.get('about')
    about_for_me = AboutMe.query.filter(AboutMe.user_id == g.user.id).all()
    if about_for_me:
        # 修改信息
        # aboutme = AboutMe()
        aboutme = about_for_me[0]
        aboutme.content = content.encode('utf-8')
        db.session.commit()
        # return render_template('user/aboutme.html', types=g.types, user=g.user)
        return render_template('user/aboutme.html')
    else:
        # 添加信息
        try:
            aboutme = AboutMe()
            aboutme.content = content.encode('utf-8')
            aboutme.user_id = g.user.id
            db.session.add(aboutme)
            db.session.commit()
        except Exception as err:
            # about_me表的外键字段user_id是唯一的，重复添加会报错。但是用判断表中是否有数据，进而分别做增加/修改动作后，此异常处理不加也行
            return redirect(url_for('user.user_center'))
        return render_template('user/aboutme.html')

# 展示关于我
@user_bp.route('/showabout')
def show_about():
    return render_template('user/aboutme.html')

# 留言板
@user_bp.route('/board', methods=['GET', 'POST'])
def show_board():
    # 获取登录用户信息<因为此路由在钩子函数里过滤了，没有强制登录，所以需要添加以下代码>
    uid = session.get('user_id', None)
    user = None
    if uid:
        user = User.query.get(uid)

    # 查询所有的留言内容
    page = int(request.args.get('page', 1))
    boards = MessageBoard.query.order_by(-MessageBoard.mdatetime).paginate(page=page, per_page=5)
    # 判断请求方式
    if request.method == 'POST':
        content = request.form.get('board')
        # 添加留言
        msg_board = MessageBoard()
        msg_board.content = content
        if uid:
            # 如果没登录留言就是匿名用户
            msg_board.user_id = uid
        db.session.add(msg_board)
        db.session.commit()
        return redirect(url_for('user.show_board'))
        # 上面重定向不用加类似user、boards的变量渲染。因为重定向是浏览器重新以get方式访问了/user/board接口，因此会访问到下面这行的。
    return render_template('user/board.html', boards=boards)

# 留言删除
@user_bp.route('/board_del')
def delete_board():
    bid = request.args.get('bid')
    if bid:
        msgboard = MessageBoard.query.get(bid)
        db.session.delete(msgboard)
        db.session.commit()
        return redirect(url_for('user.user_center'))
