import random

from flask import session
from qiniu import Auth, put_file, etag, put_data, BucketManager
import qiniu.config

from apps.article.model import Article_type
from apps.users.model import User


def upload_qiniu(filestorage):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = '3kN7t5PKDJAKhdjZVSHhh7gOq8-Tuf9bc9mUYklE'
    secret_key = 'cAH0zVZQOfGfoQSa7AXPiAL7GN9JfxgqD5yeZOAZ'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'zj-test-flask'
    # 上传后保存的文件名
    filename = filestorage.filename
    ran = random.randint(1, 1000)
    suffix = filename.rsplit('.')[-1]
    key = filename.rsplit('.')[0] + '_' + str(ran) + '.' + suffix
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, filestorage.read())
    return ret, info


def delete_qiniu(filename):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = '3kN7t5PKDJAKhdjZVSHhh7gOq8-Tuf9bc9mUYklE'
    secret_key = 'cAH0zVZQOfGfoQSa7AXPiAL7GN9JfxgqD5yeZOAZ'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'zj-test-flask'
    # 初始化BucketManager
    bucket = BucketManager(q)
    # key就是要删除的文件的名字
    key = filename
    ret, info = bucket.delete(bucket_name, key)
    return info

# 这个用不上，已经在钩子函数中拿到文章分类和用户对象，并赋值给g对象，渲染模板时可以直接取到g对象中的数据
def user_type():
    # 获取文章分类
    types = Article_type.query.all()
    # 登录用户
    user = None
    user_id = session.get('uid', None)
    if user_id:
        user = User.query.get(user_id)
    return user, types