import hashlib
import json
import time
import re
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from btoken.views import make_token
from tools.login_check import login_check


# Create your views here.
@login_check('PUT')
def readers(request, readername=None):
    if request.method == 'GET':
        if readername:
            try:
                user = Reader_Profile.objects.get(readername=readername)
            except Exception as e:
                user = None
            if not user:
                result = {'code': 208, 'error': 'no user'}
                return JsonResponse(result)
            if request.GET.keys():
                data = {}
                for k in request.GET.keys():
                    if hasattr(user, k):
                        v = getattr(user, k)
                        if k == 'avatar':
                            data[k] = str(v)
                        else:
                            data[k] = v
                result = {'code': 200, 'readername': readername, 'data': data}
                return JsonResponse(result)
            else:
                result = {'code': 200, 'readername': readername, 'data': {'gender': user.gender,
                                                                          'sign': user.sign,
                                                                          'email': user.email,
                                                                          'avatar': str(user.avatar),
                                                                          'nickname': user.nickname}}
                return JsonResponse(result)
        else:
            return JsonResponse({'code': 200, 'error': '我来了 GET'})

    elif request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {'code': 201, 'error': 'Please give me data'}
            return JsonResponse(result)
        # 把客户端拿取的json串转化为字符串
        json_obj = json.loads(json_str)

        readername = json_obj.get('readername')
        if not readername:
            result = {'code': 202, 'error': '用户名为空!'}
            return JsonResponse(result)
        # 判断用户名中不能含有特殊字符
        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', readername):
            result = {'code': 203, 'error': '用户名不可以包含非法字符(!,@,#,$,%...)'}
            return JsonResponse(result)

        # 优先查询当前用户名是否已存在
        old_user = Reader_Profile.objects.filter(readername=readername)
        if old_user:
            result = {'code': 206, 'error': '抱歉,此用户名已经存在!'}
            return JsonResponse(result)

        # email = json_obj.get('email')
        # if not email:
        #     result = {'code':203, 'error': 'Please give me email'}
        #     return JsonResponse(result)
        password_1 = json_obj.get('password01')
        password_2 = json_obj.get('password02')
        if not password_1 or not password_2:
            result = {'code': 204, 'error': '密码为空!'}
            return JsonResponse(result)

        if password_1 != password_2:
            result = {'code': 205, 'error': '两次输入的密码不一致!'}
            return JsonResponse(result)

        # 密码处理 md5哈希/散列
        m = hashlib.md5()
        m.update(password_1.encode())
        # ======charfield 尽量避免使用 null=True
        sign = gender = email = avatar = ''
        try:
            Reader_Profile.objects.create(readername=readername, nickname=readername, password=m.hexdigest(), sign=sign,
                                          gender=gender, email=email, avatar=avatar)
        except Exception as e:
            # 数据库down了， 用户名已存在
            result = {'code': 207, 'error': '服务器繁忙...'}
            return JsonResponse(result)
        # make token
        token = make_token(readername)
        # 正常返回给前端
        result = {'code': 200, 'readername': readername, 'data': {'token': token.decode()}}
        return JsonResponse(result)

        # result = {'code': 200, 'readername': readername, 'data': "测试一下路径成功"}
        # return JsonResponse(result)

    elif request.method == 'PUT':
        # http://127.0.0.1:5000/<readername>/change_info
        # 更新数据
        # 此头可获取前端传来的token
        # META可拿取http协议原生请求头,META 也是类字典对象，可使用
        # 字典相关方法
        # 特别注意 http头有可能被django重命名，建议百度
        # try:
        #
        # except:
        request.META.get('HTTP_AUTHORIZATION')

        user = request.user
        json_str = request.body
        if not json_str:
            result = {'code': 209, 'error': 'Please give me json'}
            return JsonResponse(result)

        json_obj = json.loads(json_str)

        if 'sign' not in json_obj:
            result = {'code': 210, 'error': '请输入签名'}
            return JsonResponse(result)
        if 'gender' not in json_obj:
            result = {'code': 211, 'error': '请输入性别'}
            return JsonResponse(result)
        if 'email' not in json_obj:
            result = {'code': 212, 'error': '请输入邮箱'}
            return JsonResponse(result)
        if 'nickname' not in json_obj:
            result = {'code': 212, 'error': '请输入昵称'}
            return JsonResponse(result)
        sign = json_obj.get('sign')
        gender = json_obj.get('gender')
        email = json_obj.get('email')
        nickname = json_obj.get('nickname')

        request.user.sign = sign
        request.user.gender = gender
        request.user.email = email
        request.user.nickname = nickname
        request.user.save()
        result = {'code': 200, 'readername': request.user.readername}
        return JsonResponse(result)

    else:
        raise KeyError


@login_check('POST')
def readers_avatar(request, readername):
    if request.method != "POST":
        result = {'code': 212, 'error': 'I need post'}
        return JsonResponse(result)
    avatar = request.FILES.get('avatar')
    if not avatar:
        result = {'code': 213, 'error': '请上传头像'}
        return JsonResponse(result)
    #
    request.user.avatar = avatar
    request.user.save()
    result = {'code': 200, 'readername': request.user.readername}
    return JsonResponse(result)
