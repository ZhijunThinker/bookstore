from django.shortcuts import render
from django.http import JsonResponse
from reader.models import Reader_Profile
from chapter.models import Chapter
from book.models import Book
from bookrack.models import Bookrack
from tools.login_check import login_check
import json
# Create your views here.

@login_check('GET','POST','DELETE')
def bookrack(request):
    if request.method == 'GET':
        bookracks = Bookrack.objects.filter(reader=request.user)
        res = make_bookrack_res(bookracks,request.user)
        return JsonResponse(res)
    if request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {'code': 201, 'error': 'Please give me data'}
            return JsonResponse(result)
        #把客户端拿取的json串转化为字符串
        json_obj = json.loads(json_str)
        book_id = json_obj.get('book_id')
        if not book_id:
            result = {'code':202, 'error':'没有id!'}
            return  JsonResponse(result)
        books = Book.objects.filter(id=book_id)
        if not books:
            result = {'code':203,'error':'没有这本书!'}
            return JsonResponse(result)
        book = books[0]
        book_ = Bookrack.objects.filter(book=book,reader=request.user)
        if book_:
            result = {'code':204,'error':'这本书已经在您的书架中！'}
            return JsonResponse(result)
        try:
            Bookrack.objects.create(book=book,reader=request.user)
        except Exception as e:
            result = {'code':205,'error':'服务器繁忙！'}
            return JsonResponse(result)
        result = {'code':200}
        return JsonResponse(result)
    if request.method == 'DELETE':
        # reader = request.user
        # json_str = request.body
        # if not json_str:
        #     result = {'code': 201, 'error': 'Please give me data'}
        #     return JsonResponse(result)
        # # 把客户端拿取的json串转化为字符串
        # json_obj = json.loads(json_str)
        # book_id = json_obj.get('book_id')
        # books = Book.objects.filter(id=book_id)
        # if not books:
        #     result = {'code':203,'error':'没有这本书!'}
        #     return JsonResponse(result)
        # book = books[0]
        # try:
        #     bookrack = Bookrack.objects.get(book=book,reader=reader)
        # except Exception as e:
        #     result = {'code': 205, 'error': '服务器繁忙！'}
        #     return JsonResponse(result)
        # bookrack.delete()
        # result = {'code':200}
        # return JsonResponse(result)

        reader = request.user
        json_str = request.body
        if not json_str:
            result = {'code': 201, 'error': 'Please give me data'}
            return JsonResponse(result)
        # 把客户端拿取的json串转化为字符串
        json_obj = json.loads(json_str)
        book_id = json_obj.get('book_id')
        print(book_id)
        books = Book.objects.filter(id__in=book_id)
        if not books:
            result = {'code': 203, 'error': '没有这本书!'}
            return JsonResponse(result)
        for book in books:
            try:
                bookrack = Bookrack.objects.get(book=book, reader=reader)
            except Exception as e:
                result = {'code': 205, 'error': '服务器繁忙！'}
                return JsonResponse(result)
            bookrack.delete()
        result = {'code': 200}
        return JsonResponse(result)

def make_bookrack_res(bookracks,auser):
    res = []
    user = {}
    user['name'] = auser.nickname
    user['avatar'] = str(auser.avatar)
    user['sign'] = auser.sign
    for bookrack in bookracks:
        book = bookrack.book
        data = {}
        data['id'] = book.id
        data['name'] = book.name
        data['imageUrl'] = str(book.image)
        data['is_end'] = book.is_end
        data['authorId'] = book.author.id
        data['authorName'] = book.author.name
        try:
            lastChapter = Chapter.objects.filter(book=book).last()
            data['lastChapterName'] = lastChapter.name
            data['lastChapterId'] = lastChapter.id
        except:
            data['lastChapterName'] = ''
            data['lastChapterId'] = ''
        res.append(data)
    result = {'code':200,'data':{'user':user,'book':res}}
    return result