# -*- coding: utf-8 -*-
from django.shortcuts import render
from form import LoginForm, RegisterForm, QuestionForm, AnswerForm, UpAnswerForm
from models import User, Question, Answer, QuestionType, Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import hashlib

from django.utils.timezone import utc
import datetime

from mypaginator import MyPaginator, EmptyPage, PageNotAnInteger
import qiniu
from config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME, HOSTNAME, EMAIL_SALT
from send_email import sendMail

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
    gol_error = request.GET.get('error') # 全局变量
    if name:
        # 当登陆时传递名字
        return render(request, 'index.html', {'questions': paginator, 'name': name.split()})

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
        return render(request, 'index.html', {'questions': paginator, 'name': name.split()})

    return render(request, 'index.html', {'questions': paginator, 'error': gol_error})


def getquestion(request, n):
    """问题页面"""
    questions = Question.objects.get(id=n)
    answers = questions.answer_set.all()
    name = request.session.get('name')
    if name:
        # 当登陆时传递名字
        user = User.objects.get(name=name.split()[0])
        answered = Answer.objects.filter(user=user).filter(question=questions)
        # a = Answer.objects.get(user=user)

        if answered:
            # 如果回答过了传递用户id
            return render(request,'question.html', {'questions': questions,
                                                    'answers': answers,
                                                    'name': name.split(),
                                                    'answered': user.id})
        else:
            # 没回答过显示文本编辑框
            return render(request,'question.html', {'questions': questions,
                                                    'answers': answers,
                                                    'name': name.split()})
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
        user = User.objects.get(name=name.split()[0])
        answer = Answer(user=user, question=question, text=text)
        answer.save()
        # 待修改
        return HttpResponse('ok')
    else:
        return HttpResponse('error')


def commit_post_update(request):
    """ajax更新答案"""
    name = request.session.get('name').split()
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
                    if login_error > 3 :
                        return HttpResponse('由于错误次数过多,已经帮您锁住.请%s分钟之后再试'% wait_time)
                if user.psd != hashlib.sha1(u_psd).hexdigest():
                    # 如果密码不正确查询错误次数
                    user.login_error += 1
                    user.save()
                    # remainder = 4 - login_error
                    return HttpResponse('邮箱或密码错误')
                else:
                    # 登录成功
                    name = user.name
                    request.session['name'] = name+" "+str(user.id)
                    user.last_time = 0
                    user.save()
                    return JsonResponse({'status': 'ok'})
            except User.DoesNotExist:
                return HttpResponse('邮箱或密码错误')


def register(request):
    """注册用户"""
    if request.method == "POST":
        f = RegisterForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data["name"]   # 用户名
            email = f.cleaned_data["email"] # 邮箱
            psd = f.cleaned_data["psd"] # 密码
            real_ip = request.META['REMOTE_ADDR']   #ip
            introduction = f.cleaned_data["introduction"]
            vericode = hashlib.sha1(email+EMAIL_SALT).hexdigest()
            user = User.objects.create(name=name, email=email, psd=hashlib.sha1(psd).hexdigest(),
                                       introduction=introduction, vericode=vericode, real_ip=real_ip)
            if sendMail([email], '验证邮箱', '<a href="http://{HOSTNAME}/validate/{vericode}">验证邮箱</a>'.format(HOSTNAME=HOSTNAME, vericode=vericode)):
                user.save()
            else:
                pass# 邮件发送失败
            return HttpResponseRedirect("/")
        else:
            return render(request, "register.html", {'errors': f.errors})
    return render(request, "register.html")


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
        name = request.session.get("name").split()
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
            user = User.objects.get(name=name.split()[0])
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
        return render(request,'askquestion.html',{'QuestionForm':QuestionForm, 'name':name.split()})
    else:
        return HttpResponseRedirect("/")


def programmer(request, n):
    # 个人主页
    user = User.objects.filter(id=n)            # 这个返回的是数组
    answers = user[0].answer_set.all()          # 一定要加[0]编程一个对象
    answers_count = len(answers)
    questions = user[0].question_set.all()
    questions_count = len(questions)
    name = request.session.get("name")
    q = request.GET.get('q')
    if user:
        if not q or q == 'answers':
            return render(request, 'programmer.html', {'user': user[0], 'answers': answers, 'name': name.split(),
                                                       "answers_count": answers_count,
                                                       "questions_count": questions_count})
        elif q == 'questions':
            return render(request, 'programmer_questions.html', {'user': user[0], 'name': name.split(),
                                                                 'questions': questions,
                                                                 "questions_count": questions_count,
                                                                 "answers_count": answers_count})
        else:
            pass  # 还要添加一些东西
    else:
        return HttpResponseRedirect("/")


def agree_answer(request):
    # 增加赞同的数 2增加赞同的人
    name = request.session.get('name')
    # 如果登录了,就变动
    if name:
        answer_id = request.GET.get('aid')
        tag = request.GET.get('tag')    # 加还是减
        answer = Answer.objects.get(id=answer_id)
        user = User.objects.get(id=name.split()[1])
        # 如果传递1就加
        if tag == '1':
            if not Answer.objects.filter(agree_user=user).filter(id=answer_id):
                answer.agree_num += 1
                answer.agree_user.add(user)
                answer.save()
                jsonData = {'status': 'ok'}
                return JsonResponse(jsonData)
            else:
                return HttpResponse("已经赞同过了↖(^ω^)↗")
        else:
            if Answer.objects.filter(agree_user=user).filter(id=answer_id):
                answer.agree_num -= 1
                answer.agree_user.remove(user)
                answer.save()
                jsonData = {'status': 'ok'}
                return JsonResponse(jsonData)
            else:
                return HttpResponse("已经取消赞同啦")
    else:
        return HttpResponse("可以麻烦您登陆下么⊙︿⊙")


def getcomment(request):
    # 得到评论
    return HttpResponse('ok')


def addcomment(request):
    name = request.session.get('name')
    if name and request.method == 'POST':
        aid = request.POST.get('aid')
        text = request.POST.get('text')
        user = User.objects.get(name=name.split()[0])
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
    return HttpResponse(code)
