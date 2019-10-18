import hashlib
import json
import time

from django.http import JsonResponse
from django.shortcuts import render
from reader.models import Reader_Profile


# Create your views here.
def tokens(request):

    if not request.method == 'POST':
        result = {'code': 101 , 'error': 'Please use POST'}
        return JsonResponse(result)

    json_str = request.body
    if not json_str:
        result = {'code': 102, 'error': 'Please give me json'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)
    readername = json_obj.get('readername')
    password = json_obj.get('password')
    if not readername:
        result = {'code':103, 'error': '请输入用户名'}
        return JsonResponse(result)
    if not password:
        result = {'code':104, 'error': '请输入密码'}
        return JsonResponse(result)

    user = Reader_Profile.objects.filter(readername=readername)
    if not user:
        result = {'code':105, 'error': '用户名或密码错误!! '}
        return JsonResponse(result)

    user = user[0]
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        result = {'code': 106, 'error': '用户名或密码错误!!!'}
        return JsonResponse(result)
    token = make_token(readername)
    result = {'code':200, 'readername':readername, 'data':{'token':token.decode()}}
    return JsonResponse(result)


def make_token(readername, expire=3600 * 24):
    # 官方jwt / 自定义jwt
    import jwt
    key = '1234567'
    now = time.time()
    payload = {'readername': readername, 'exp': int(now + expire)}
    return jwt.encode(payload, key, algorithm='HS256')

































