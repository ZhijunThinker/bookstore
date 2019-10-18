import json

from django.http import JsonResponse
from django.shortcuts import render

from tools.login_check import login_check
from reader.models import Reader_Profile
from book.models import Book
from .models import Comment


# Create your views here.
@login_check('POST')
def comments(request, book_id):
    if request.method != 'POST':
        result = {'code': 401, 'error': 'Please use POST'}
        return JsonResponse(result)

    # 发表留言/回复
    # 获取用户
    user = request.user
    json_str = request.body
    # load回python obj
    json_obj = json.loads(json_str)
    content = json_obj.get('content')
    if not content:
        result = {'code': 402, 'error': 'Please give me content'}
        return JsonResponse(result)
    try:
        book = Book.objects.get(id=book_id)
    except:
        # topic被删除 or 当前topic_id 不真实
        result = {'code': 403, 'error': 'No No Book!'}
        return JsonResponse(result)

    # 创建数据
    Comment.objects.create(content=content, reader=user, book=book)

    return JsonResponse({'code': 200, 'data': {}})
