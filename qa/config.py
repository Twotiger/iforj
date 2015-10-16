# -*- coding: utf-8 -*
# 七牛支持
ACCESS_KEY = "wmN715-Lo5SC1jYIkuqObCLl1bhZoURTxewUGyq2"
SECRET_KEY = "IXXeA4-Rzu9RB6nkf687UjQt9YCOp1JpWptm0C0y"
BUCKET_NAME = "iforj"

# 邮箱支持
MAIL_HOST = "smtp.163.com"
MAIL_USER = "duangguangmoon"
MAIL_PASS = "duangguang"
MAIL_POSTFIX = "163.com"    # 邮箱的后半段
HOSTNAME = "127.0.0.1"  # HOSTNAME

# EMAIL_CONTENT = '<a href="http://{HOSTNAME}/validate/{vericode}">验证邮箱</a>'
# .format(HOSTNAME=HOSTNAME, vericode=user.vericode)

# 注册
EMAIL_SALT = "AF4E%W8-9"    # 随机生成

# IMAGE_BASE_PATH = "/static/gavin/Documents/github/Django/iforj/qa/static/img/upload/"
# IMAGE_APPLICATION_PATH = "/static/img/upload/"
# DEFAULT_IMAGE_PATH = "/static/img/upload/default.jpg"

IMAGE_BASE_PATH = "qa/static/img/upload/"
IMAGE_APPLICATION_PATH = "/static/img/upload/"
DEFAULT_IMAGE_PATH = "/static/img/upload/default.jpg"

DENY_USER_NAME = [u'管理', u'admin', u'root', u'匿名', u'版主', u'站长', u'屌', u'屄', u'fuck']   # 禁止的用户名
