from flask import Blueprint, request, g, redirect, url_for, render_template, jsonify, session
from . import article_bp
from apps.article.model import Article, Article_type, Comment
from ..users.model import User
from exts import db


# 自定义过滤器
# 整个app都能使用，而不是只对某个蓝图可用
from ..utils.util import user_type


@article_bp.app_template_filter('cdecode')
def content_decode(content):
    content = content.decode('utf-8')
    return content[:200]


@article_bp.route('/publish', methods=['POST', 'GET'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        type_id = request.form.get('type')
        # 数据库字段为blob，因此需要编码后才能写入db
        content = request.form.get('content').encode('utf8')
        # 添加文章
        article = Article()
        article.title = title
        article.type_id = type_id
        article.content = content
        article.user_id = g.user.id
        db.session.add(article)
        db.session.commit()
        # return 'add ok'
        return redirect(url_for('user.index'))
    else:
        return render_template('article/add_article.html')

@article_bp.route('/detail')
def article_detail():
    # 获取文章对象通过id
    article_id = request.args.get('aid')
    article = Article.query.get(article_id)
    # # 获取文章分类
    # types = Article_type.query.all()
    # 获取用户
    # user_id = session.get('user_id',None)
    # user = None
    # if user_id:
    #     user = User.query.get(user_id)
    # 单独查询评论
    page = int(request.args.get('page', 1))
    comments = Comment.query.filter(Comment.article_id == article_id) \
        .order_by(-Comment.cdatetime) \
        .paginate(page=page, per_page=5)
    return render_template('article/detail.html', article=article, comments=comments)


@article_bp.route('/love')
def article_love():
    article_id = request.args.get('aid')
    tag = request.args.get('tag')

    article = Article.query.get(article_id)
    if tag == '1':
        article.love_num -= 1
    else:
        article.love_num += 1
    db.session.commit()
    return jsonify(num=article.love_num)

# 发表文章评论
@article_bp.route('/add_comment', methods=['GET', 'POST'])
def article_comment():
    if request.method == 'POST':
        comment_content = request.form.get('comment')
        user_id = g.user.id
        article_id = request.form.get('aid')
        # 评论模型
        comment = Comment()
        comment.comment = comment_content
        comment.user_id = user_id
        comment.article_id = article_id
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article.article_detail') + "?aid=" + article_id)
    # 此接口不需要get方法，因此上面的get和下面这行都可以删除的
    return redirect(url_for('user.index'))

# 文章分类检索
@article_bp.route('/type_search')
def type_search():
    # 获取用户和文章类型给导航使用。封装一个函数获取用户和文章类型用于渲染模板。但是采用了g.user/g.types后已经不需要这样做了。
    # user, types = user_type()
    # tid的获取
    tid = request.args.get('tid', 1)
    page = int(request.args.get('page', 1))
    # pagination对象
    articles = Article.query.filter(Article.type_id == tid).paginate(page=page, per_page=3)

    # params = {
    #     'user': user,
    #     'types': types,
    #     'articles': articles,
    #     'tid': tid,
    # }
    # 因为钩子函数中获取了user,types，所以下面字典中不用加了，在html模板中直接用g对象获取
    params = {
        'articles': articles,
        'tid': tid,
    }
    # **取字典的每个键值对，*取数组的每个值
    return render_template('article/article_type.html', **params)
