# -*- coding: utf-8 -*-
from django.shortcuts import render
from form import LoginForm, RegisterForm, QuestionForm
from models import User, Question, Answer,QuestionType
from django.http import HttpResponse, HttpResponseRedirect
import hashlib
# from django_qiniu.fields import QiNiuImageField, QiniuFileField
import qiniu

# Create your views here.
def index(request):
    """Q&A首页"""
    name =request.session.get('name')
    page = Question.objects.all()
    gol_error = request.GET.get('error')
    if name:
        # 当登陆时传递名字
        return render(request,'index.html',{'page': page, 'name': name})

    return render(request,'index.html',{'page': page, 'error':gol_error})


#后期再改
def testtwo():
    access_key = "wmN715-Lo5SC1jYIkuqObCLl1bhZoURTxewUGyq2"
    secret_key = "IXXeA4-Rzu9RB6nkf687UjQt9YCOp1JpWptm0C0y"
    bucket_name = "iforj"
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket_name)
    return token



def getquestion(request, n):
    """问题页面"""
    questions = Question.objects.get(id=n)
    answers = questions.answer_set.all()
    name =request.session.get('name')
    if name:
        # 当登陆时传递名字
        user = User.objects.get(name=name)
        answered = Answer.objects.filter(user=user).filter(question=questions)
        if answered:
            # 如果回答过了传递用户id
            return render(request,'question.html', {'questions': questions,
                                                    'answers': answers,
                                                    'name': name,
                                                    'answered': user.id})
        else:
            return render(request,'question.html', {'questions': questions,
                                                    'answers': answers, 'uptoken':testtwo(),
                                                    'name': name })
    else:
        return render(request,'question.html', {'questions': questions,
                                                'answers': answers})

def commit_post_add(request):
    """ajax提交答案"""
    name = request.session.get('name')
    if request.method == "POST" and name:
        qid = request.POST.get('qid')
        text = request.POST.get('text')
        # text = html.replace('<', '&lt;').replace('>', '&gt;') #待改
        question = Question.objects.get(id=int(qid))
        # 答案数 + 1
        question.q_times += 1
        question.save()
        # 保存到数据库
        user = User.objects.get(name=name)
        answer = Answer(user=user, question=question, text=text)
        answer.save()
        # 待修改
        return HttpResponse('ok')
    else:
        return HttpResponse('error')




def login(request):
    """登陆只接受POST,无法正常访问"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u_email = data['email']
            u_psd = data['password']

            user = User.objects.filter(email=u_email, psd= hashlib.sha1(hashlib.sha1(u_psd).hexdigest()  ).hexdigest())
            if user:
                # response = HttpResponseRedirect('/')
                response =HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                name = User.objects.get(email=u_email).name
                request.session['name'] = name
                return response
            else:
                return HttpResponseRedirect("/"+"?error=loginerror&a=%s"%hashlib.sha1(u_psd).hexdigest())
                return HttpResponseRedirect("/"+"?error=loginerror")

def register(request):
    """注册用户"""
    if request.method == "POST":
        f = RegisterForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data["name"]
            email = f.cleaned_data["email"]
            psd = f.cleaned_data["psd"]
            introduction = f.cleaned_data["introduction"]
            user = User.objects.create(name=name, email=email, psd=psd, introduction=introduction)
            user.save()
            return HttpResponseRedirect("/")
        else:
            return render(request,"register.html",{'errors': f.errors})
    return render(request,"register.html")

def search(request):
    """搜索问题"""
    search_type = request.GET.get('type')
    q = request.GET.get('q')
    if not search_type:
        search_type = "question"

    name = None
    if request.session.get("name"):
        name = request.session.get("name")

    if search_type == "question":
        questions = Question.objects.filter(title__contains=q)
        return render(request,'search.html',{'questions': questions,'q':q,'flag':'question',"name":name})
    elif search_type == "people":
        users = User.objects.filter(name__contains=q)
        return render(request,"search.html",{'users': users,'q': q,'flag':'people',"name":name})
    else:
        topics = QuestionType.objects.filter(name__contains=q)
        return render(request,"search.html",{'topics': topics,"q": q,'flag':'topic',"name":name})

def logout(request):
    """登出"""
    del request.session['name']
    return HttpResponseRedirect('/')    # 改成刷新 或者 js

def getcomment(request):
    return HttpResponse('ok')



def askquestion(request):
    """提问模板"""
    name =request.session.get('name')
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data['title']
            text = data['text']
            qtype = data['q_type']
            # title = request.POST.get('title')
            # text = request.POST.get('text')
            # q_type = data['q_type']
            user = User.objects.get(name=name)
            questiontype = QuestionType.objects.get(id=qtype)

            question = Question(user=user, title=title, text=text, q_type=questiontype)

            question.save()
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return HttpResponseRedirect("/") #待改
        else:
            return HttpResponse(request.POST.get('title'))
    if name:
        access_key = "wmN715-Lo5SC1jYIkuqObCLl1bhZoURTxewUGyq2"
        secret_key = "IXXeA4-Rzu9RB6nkf687UjQt9YCOp1JpWptm0C0y"
        bucket_name = "iforj"
        q = qiniu.Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)
        return render(request,'askquestion.html',{'QuestionForm':QuestionForm, 'uptoken':token,'name':name})
    else:
        return HttpResponseRedirect("/")
"""
    user = models.ForeignKey(User)
    title = models.CharField(max_length=127)
    text = models.TextField()
    q_datetime = models.DateTimeField(auto_now=True) # 回复时间
    q_times = models.PositiveSmallIntegerField(default=0)   # 回复数量
    q_type = models.ForeignKey(QuestionType, null=True, blank=True)
"""



