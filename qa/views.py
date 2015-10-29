# -*- coding: utf-8 -*-
from django.shortcuts import render
from form import LoginForm, RegisterForm, QuestionForm, AnswerForm, UpAnswerForm, UploadImageForm, EditProfileForm
from models import User, Question, Answer, QuestionType, Comment
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse

import hashlib
import tempfile

from django.utils.timezone import utc
from PIL import Image, ImageDraw, ImageFont


import datetime

from mypaginator import MyPaginator, EmptyPage, PageNotAnInteger
import qiniu, os
from config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME, HOSTNAME, EMAIL_SALT, IMAGE_BASE_PATH, \
                                    IMAGE_APPLICATION_PATH, DEFAULT_IMAGE_PATH, FONT_PATH
from send_email import sendMail

from cStringIO import StringIO
import random
# Create your views here.


def index(request):
    """Q&A首页"""
    name =request.session.get('name')

    # 显示最新
    questions = Question.objects.all()
    # 分页
    paginator  = MyPaginator(questions, 10)

    page = request.GET.get('page')
    try:
        paginator.page(page)
    except PageNotAnInteger:
        paginator.page(1)
    except EmptyPage:
        paginator.page(paginator.num_pages)
    gol_error = request.GET.get('error')  # 全局变量
    if name:
        # 当登陆时传递名字
        return render(request, 'index.html', {'questions': paginator, 'name': name.split("&")})

    return render(request, 'index.html', {'questions': paginator, 'error': gol_error})


def top(request):
    """TOP"""
    name = request.session.get('name')
    qtype = request.GET.get('type')

    questions = Question.objects.all().order_by('-q_times')
    # 分页
    paginator = MyPaginator(questions, 10)
    page = request.GET.get('page')
    try:
        paginator.page(page)
    except PageNotAnInteger:
        paginator.page(1)
    except EmptyPage:
        paginator.page(paginator.num_pages)
    gol_error = request.GET.get('error')
    if name:
        # 当登陆时传递名字
        return render(request, 'index.html', {'questions': paginator, 'name': name.split("&")})

    return render(request, 'index.html', {'questions': paginator, 'error': gol_error})


def getquestion(request, n):
    """问题页面"""
    try:
        questions = Question.objects.get(id=n)
    except:
        raise Http404('错误的url')
    answers = questions.answer_set.all()
    name = request.session.get('name')
    if name:
        # 当登陆时传递名字
        user = User.objects.get(name=name.split("&")[0])
        followings = user.following.all()
        fans = user.follower.all()
        following_count = len(followings)
        followed_count = len(fans)
        answered = Answer.objects.filter(user=user).filter(question=questions)
        # a = Answer.objects.get(user=user)

        if answered:
            # 如果回答过了传递用户id
            return render(request,'question.html', {'questions': questions,
                                                    'answers': answers,
                                                    'name': name.split("&"),
                                                    'answered': user.id})
        else:
            # 没回答过显示文本编辑框
            return render(request,'question.html', {'questions': questions,
                                                    'answers': answers,
                                                    'name': name.split("&")})
    else:
        # 没登陆
        return render(request,'question.html', {'questions': questions,
                                                'answers': answers})


def commit_post_add(request):
    """ajax提交答案"""
    name = request.session.get('name')
    form = AnswerForm(request.POST)
    if request.method == "POST" and name and form.is_valid():
        data = form.cleaned_data
        qid = data['qid']
        text = data['text']
        # text = html.replace('<', '&lt;').replace('>', '&gt;') #待改
        question = Question.objects.get(id=int(qid))
        # 答案数 + 1
        question.q_times += 1
        question.save()
        # 保存到数据库
        user = User.objects.get(name=name.split("&")[0])
        answer = Answer(user=user, question=question, text=text)
        answer.save()
        # 待修改
        return HttpResponse('ok')
    else:
        return HttpResponse('error')


def commit_post_update(request):
    """ajax更新答案"""
    name = request.session.get('name').split("&")
    form = UpAnswerForm(request.POST)

    if request.method == "POST" and name and form.is_valid():
        data = form.cleaned_data
        aid = data['get_id']
        text = data['text']
        answer = Answer.objects.get(id=aid)
        if answer:
            answer.text = text
            answer.save()
            return JsonResponse({'status': 'ok'})
    else:
        return HttpResponse('ERROR')


def login(request):
    """登陆只接受POST,无法正常访问"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u_email = data['email']
            u_psd = data['password']
            # return render(request, 'index.html',{'login_error':request.META.get('HTTP_REFERER', '/')})
            try:
                user = User.objects.get(email=u_email)
                # 登录错误检查
                login_error = user.login_error
                last_time = user.last_time
                now = datetime.datetime.utcnow().replace(tzinfo=utc)
                del_s = now - last_time
                wait_time = (login_error - 3) * 5
                if del_s.seconds > wait_time * 60:
                    # 如果相差的时间大于必须等待的秒数,可以正常登录一次
                    pass
                else:
                    if login_error > 3:
                        return HttpResponse('由于错误次数过多,已经帮您锁住.请%s分钟之后再试'% wait_time)
                if user.psd != hashlib.sha1(u_psd).hexdigest():
                    # 如果密码不正确查询错误次数
                    user.login_error += 1
                    user.save()
                    # remainder = 4 - login_error
                    return HttpResponse('邮箱或密码错误')
                else:
                    # 检查是否验证了邮箱
                    if not user.is_veri:
                        return HttpResponse("可以麻烦您验证一下邮箱么⊙︿⊙")
                    else:
                        # 登录成功
                        name = user.name
                        request.session['name'] = name + "&" + str(user.id)  # 总觉得空格不太好
                        # print name
                        user.last_time = 0
                        user.save()
                        return JsonResponse({'status': 'ok'})
            except User.DoesNotExist:
                return HttpResponse('邮箱或密码错误')
        else:
            return HttpResponse('邮箱或密码错误')


def register(request):
    """注册用户"""
    if request.method == "POST":
        f = RegisterForm(request.POST)

        if f.is_valid():
            vari = request.POST.get('vari')
            if not vari or vari != request.session.get("captcha"):
                # return render(request, "register.html", {'errors': f.errors})
                return render(request, "register.html", {'errors': '错误的验证码'})
            name = f.cleaned_data["name"]    # 用户名
            email = f.cleaned_data["email"]  # 邮箱
            psd = f.cleaned_data["psd"]  # 密码
            real_ip = request.META['REMOTE_ADDR']   # ip
            introduction = f.cleaned_data["introduction"]
            vericode = hashlib.sha1(email+EMAIL_SALT).hexdigest()
            user = User.objects.create(name=name, email=email, psd=hashlib.sha1(psd).hexdigest(),
                                       introduction=introduction, vericode=vericode, real_ip=real_ip,
                                       image=DEFAULT_IMAGE_PATH)

            if sendMail([email], '验证邮箱', u"""{username},你好,IFORJ是致力于python的网络问答社区,帮助你寻找答案,分享知识。iforj是由用户可以根据自身的需
求,有针对性地提出问题;同时,这些答案又将作为搜索结果。你可以搜索类似的问题，问题被分为，爬虫，数据分析，django，scrapy，
python语法等基础分类，你可以按着分类搜索相关的问题。我们以打造最活跃的python问答平台为目的，很高兴为您提供便捷的服务。
如果有好的意见和建议，欢迎联系我们
<a href="http://{HOSTNAME}/validate/{vericode}">验证邮箱</a>""".format(username=name,
                    HOSTNAME=HOSTNAME, vericode=vericode)):
                del request.session['captcha']
                user.save()
            else:
                pass  # 邮件发送失败
            return HttpResponseRedirect("/")
        else:
            return render(request, "register.html", {'errors': f.errors})
    return render(request, "register.html")


def editProfile(request):
    name = request.session.get("name")
    if name:
        user_id = name.split("&")[1]
    else:
        user_id = None
    user = User.objects.get(id=user_id)
    old_email = user.email
    old_introduction = user.introduction

    if request.method == "POST":
        f = EditProfileForm(request.POST)
        if f.is_valid():
            new_email = f.cleaned_data["new_email"]
            new_introduction = f.cleaned_data["new_introduction"]
            user.email = new_email
            user.vericode = hashlib.sha1(new_email+EMAIL_SALT).hexdigest()
            user.introduction = new_introduction
            user.save()
            return HttpResponseRedirect("/programmer/%s" % str(user_id))
        else:
            return render(request, "edit-profile.html", {'errors': f.errors, "name": name.split("&")})
    return render(request, "edit-profile.html", {"email": old_email, "introduction": old_introduction,
                                                 "name": name.split("&")})


def mypaginator(request, questions, n):
    paginator  = MyPaginator(questions, n)
    page = request.GET.get('page')
    try:
        paginator.page(page)
    except PageNotAnInteger:
        paginator.page(1)
    except EmptyPage:
        paginator.page(paginator.num_pages)
    return paginator


def search(request):
    """搜索问题"""
    search_type = request.GET.get('type')
    q = request.GET.get('q')
    if not search_type:
        search_type = "question"

    if request.session.get("name"):
        name = request.session.get("name").split("&")
    else:
        name = None

    if search_type == "question":
        questions = Question.objects.filter(title__icontains=q)

        paginator = mypaginator(request, questions, 10)
        return render(request,'search.html',{'questions': paginator,'q':q,'flag':'question',"name":name})

    elif search_type == "people":
        users = User.objects.filter(name__contains=q)
        return render(request, "search.html", {'users': users, 'q': q, 'flag': 'people', "name": name})
    else:
        topics = QuestionType.objects.filter(name__icontains=q)
        try:
            questiontype = QuestionType.objects.get(name=q)
            questions = questiontype.question_set.all()
        except Exception:
            questions = []
        questions_num = len(questions) # 共多少问题
        paginator = MyPaginator(questions, 10)
        page = request.GET.get('page')
        try:
            paginator.page(page)
        except PageNotAnInteger:
            paginator.page(1)
        except EmptyPage:
            paginator.page(paginator.num_pages)

        #        questions = Question.objects.filter(q_type = q)
        return render(request,"search.html",{'topics': topics, "q": q, 'flag':'topic',
                                             "name":name, 'questions': paginator, 'questions_num':questions_num })


def logout(request):
    """登出"""

    del request.session['name']
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))   # 改成 js


def askquestion(request):
    """提问模板"""
    name =request.session.get('name')
    if request.method == "POST" and request.is_ajax():

        form = QuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data['title']
            text = data['text']
            qtype = data['q_type'].lower()
            user = User.objects.get(name=name.split("&")[0])
            try:
                questiontype = QuestionType.objects.get(name=qtype)
            except QuestionType.DoesNotExist:
                questiontype = QuestionType(name=qtype)
                questiontype.save()

            question = Question(user=user, title=title, text=text, q_type=questiontype)
            question.save()

            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return JsonResponse({'status':'ok'})
        else:
            # return HttpResponse(request.POST.get('title'))
            return render(request, 'askquestion.html')
    if name:
        return render(request,'askquestion.html',{'QuestionForm':QuestionForm, 'name':name.split("&")})
    else:
        return HttpResponseRedirect("/")


def programmer(request, n):
    # 个人主页
    user = User.objects.filter(id=n)            # 这个返回的是数组
    answers = user[0].answer_set.all()          # 一定要加[0]编程一个对象
    answers_count = len(answers)
    questions = user[0].question_set.all()
    questions_count = len(questions)
    followings = user[0].following.all()
    fans = user[0].follower.all()
    following_count = len(followings)
    followed_count = len(fans)
    if request.session.get("name"):
        name = request.session.get("name").split("&")
    else:
        name = None
    # 当前用户是否关注过此用户
    if name is not None:
        followed = User.objects.filter(id=n)
        following = User.objects.filter(id=name[1])
        if following.filter(following=followed):
            is_following = True
        else:
            is_following = False
    else:
        is_following = False
    q = request.GET.get('q')
    if user:
        if not q or q == 'questions':
            return render(request, 'programmer_questions.html', {'user': user[0], 'name': name,
                                                                 'questions': questions,
                                                                 "questions_count": questions_count,
                                                                 "answers_count": answers_count,
                                                                 "following_count": following_count,
                                                                 "followed_count": followed_count,
                                                                 "is_following": is_following})
        elif q == "following":
            return render(request, "programmer_following.html", {'user': user[0], 'name': name,
                                                                 "followings": followings,
                                                                 "questions_count": questions_count,
                                                                 "answers_count": answers_count,
                                                                 "following_count": following_count,
                                                                 "followed_count": followed_count,
                                                                 "is_following": is_following})
        elif q == "fan":
            return render(request, "programmer_fan.html", {'user': user[0],
                                                           'name': name,
                                                           "fans": fans,
                                                           "questions_count": questions_count,
                                                           "answers_count": answers_count,
                                                           "following_count": following_count,
                                                           "followed_count": followed_count,
                                                           "is_following": is_following})
        else:
            pass

    else:
        return HttpResponseRedirect("/")


def uploadImage(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        # print form
        if form.is_valid():
            n = form.cleaned_data["user_id"]
            user = User.objects.get(id=n)
            f = request.FILES["user_image"]
            name = f.name
            size = f.size / (1024.0*1024.0)

            # 判断图片大小
            if size > 2.0:
                return HttpResponse("<p>图片大小不能超过2M!</p>")

            image = Image.open(f)
            image.thumbnail((128, 128), Image.ANTIALIAS)
            image_newname = "%s." % str(n) + name.split(".")[1]
            image_path = IMAGE_BASE_PATH + image_newname
            image.save(image_path)
            user.image = IMAGE_APPLICATION_PATH + image_newname
            user.save()
            return HttpResponseRedirect("/programmer/%s" % str(n))
        elif "请上传一张有效的图片".decode("utf-8") in form.errors["user_image"][0]:
            return HttpResponse("<p>请上传一张有效的图片。您所上传的文件不是图片或者是已损坏的图片!<p>")
        elif "这个字段是必填项".decode("utf-8") in form.errors["user_image"][0]:
            return HttpResponse("<p>请选择文件!</p>")
        else:
            return HttpResponse("<p>发生未知错误!</p>")


def agree_answer(request):
    # 增加赞同的数 2增加赞同的人
    # {'aid':aid, 'tag':1}
    name = request.session.get('name')
    # 如果登录了,就变动
    if name:
        answer_id = request.GET.get('aid')
        tag = request.GET.get('tag')    # 加还是减
        answer = Answer.objects.get(id=answer_id)   # 得到答案
        user = User.objects.get(id=name.split("&")[1])
        # 如果传递1就加
        if tag == '1':
            if not Answer.objects.filter(agree_user=user).filter(id=answer_id):
                answer.agree_num += 1
                answer.agree_user.add(user)
                answer.save()

                user = User.objects.get(id=answer.user.id)  # 给回答的用户添加agree_num
                user.agree_num += 1
                user.save()

                jsonData = {'status': 'ok'}
                return JsonResponse(jsonData)
            else:
                return HttpResponse("已经赞同过了↖(^ω^)↗")
        else:
            if Answer.objects.filter(agree_user=user).filter(id=answer_id):
                answer.agree_num -= 1
                answer.agree_user.remove(user)
                answer.save()

                user = User.objects.get(id=answer.user.id)  # 给回答的用户减agree_num
                user.agree_num -= 1
                user.save()

                jsonData = {'status': 'ok'}
                return JsonResponse(jsonData)
            else:
                return HttpResponse("已经取消赞同啦")
    else:
        return HttpResponse("可以麻烦您登陆下么⊙︿⊙")


def follow(request, n):
    if request.session.get("name"):
        name = request.session.get("name").split("&")
    else:
        return HttpResponse("可以麻烦您登陆下么⊙︿⊙")
    followed = User.objects.filter(id=n)
    following = User.objects.filter(id=name[1])
    if not following.filter(following=followed):
        following[0].following.add(followed[0])
        followed[0].follower.add(following[0])
        following[0].save()
        followed[0].save()
        jsonData = {"status": "ok"}
        return JsonResponse(jsonData)
    else:
        return HttpResponse("wrong")


def unfollow(request, n):
    if request.session.get("name"):
        name = request.session.get("name").split("&")
    else:
        return HttpResponse("可以麻烦您登陆下么⊙︿⊙")
    followed = User.objects.filter(id=n)
    following = User.objects.filter(id=name[1])
    if following.filter(following=followed):
        following[0].following.remove(followed[0])
        followed[0].follower.remove(following[0])
        following[0].save()
        followed[0].save()
        jsonData = {"status": "ok"}
        return JsonResponse(jsonData)
    else:
        return HttpResponse("wrong")


def getcomment(request):
    # 得到评论
    return HttpResponse('ok')


def addcomment(request):
    name = request.session.get('name')
    if name and request.method == 'POST':
        aid = request.POST.get('aid')
        text = request.POST.get('text')
        user = User.objects.get(name=name.split("&")[0])
        answer = Answer.objects.get(id=aid)
        comment = Comment(user=user, text=text, answer=answer)
        comment.save()
        return JsonResponse({'status': 'ok'})
    else:
        return HttpResponse('not login')


def about_us(request):
    return render(request, 'about_me.html')


def test(request):
    # ip = request.META['HTTP_X_FORWARDED_FOR']
    ip = request.META['REMOTE_ADDR']
    return render(request,'test.html', {'ip':ip})


def qntoken(request):
    q = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME)
    jsonData = {"uptoken":token}
    return JsonResponse(jsonData)


def validate(request, code):
    """验证"""
    user = User.objects.filter(vericode=code)
    if user:
        user[0].is_veri = True
        user[0].save()
        return HttpResponse("<p>您已成功验证!&nbsp;&nbsp;<a href='/'>返回首页</a></p>")

# def veriimage():
#     text = u''
#     fontName = 'black.ttf'
#     buf = cStringIO.StringIO()
#
#     font = PIL.ImageFont.truetype(fontName, fontSize)
#     width, height = font.getsize(text)
#     logging.debug('(width, height) = (%d, %d)' % (width, height))
#     image = PIL.Image.new('RGBA', (width, height), (0, 0, 0, 0))  # 设置透明背景
#     draw = PIL.ImageDraw.Draw(image)
#     draw.text((0, -4), text, font = font, fill = '#000000')
#     image.save(buf, "GIF")


def verificationcode(request):
    """验证码"""
    a = random.randint(-99,99)
    b = random.randint(1,99)
    midd = random.choice(['+', '-', '*' , '**'])
    text = u'%s %s %s'% (a, midd, b)
    #fontName = 'qa/static/fonts/black.ttf'   # 如果没有这个字体会出现IOError
    #  fontName = 'Yahei Consolas Hybrid.ttf'   # 如果没有这个字体会出现IOError
    # fontName = 'qa/static/black.ttf'
    fontSize = 37
    buf = StringIO()
    font = ImageFont.truetype('qa/static/fonts/black.ttf', fontSize)
    width, height = font.getsize(text)
    image = Image.new('RGBA', (width, height), (255, 255, 255, 255))  # 设置透明背景
    draw = ImageDraw.Draw(image)
    draw.text((0, -4), text, font = font, fill = '#000000')
    image.save(buf, "GIF")

    imagedata = buf.getvalue()
    buf.close()
    request.session['captcha'] = str(eval(text))
    response = HttpResponse(imagedata, 'image/jpeg')
    # response.set_cookie('captcha', eval(text))
    return response
