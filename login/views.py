# login/views.py

from django.shortcuts import render, redirect
from .models import User
from . import forms
import hashlib


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        if request.session['user_name'] == 'admin':
            return redirect('/admin_index/')
        else:
            return redirect('/user_index/')

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            if login_form.cleaned_data['username'] == 'admin':
                if User.objects.get(name=username):
                    user = User.objects.get(name=username)
                    if user.password == hash_code(password): # 哈希值和数据库内的值进行比对
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.name
                        # login(request, user)
                        return redirect('/admin_index/')
                    else:
                        message = "密码不正确！"
                else:
                    message = "请创建管理员账号！"
            else:
                if User.objects.get(name=username):
                    user = User.objects.get(name=username)
                    if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.name
                        # login(request, user)
                        return redirect('/user_index/')
                    else:
                        message = "密码不正确！"
                else:
                    message = "用户不存在！"

        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    # 登录状态不允许注册。可以修改这条原则。
    if request.session.get('is_login', None):
        if request.session['user_name'] == 'admin':
            return redirect('/admin_index/')
        else:
            return redirect('/user_index/')

    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/user_index/')
    request.session.flush()
    # logout(request)

    return redirect('/user_index/')


def hash_code(s, salt='mysite_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()