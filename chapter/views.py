from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from book.models import Book
from chapter.models import Chapter
from tools.parse_classification import parse_classification
from tools.login_check import login_check


# Create your views here.
# @login_check('GET')
def chapter(request, book_id, chapter_id):
    if request.method == 'GET':
        books_obj = Book.objects.filter(id=book_id)[0]
        chapters_obj = Chapter.objects.filter(id=chapter_id)[0]
        if books_obj == []:
            return JsonResponse({'code': 301, 'error': 'no this book'})
        elif chapters_obj == []:
            return JsonResponse({'code': 302, 'error': 'no this chapter'})
        elif chapters_obj.book.id != books_obj.id:
            return JsonResponse({'code': 303, 'error': 'chapter is not belong to this book'})
        else:
            chapters = books_obj.chapter_set.all()
            chapter_ids = []
            for chapter in chapters:
                chapter_ids.append(chapter.id)
            try:
                chapter_id = int(chapter_id)
            except:
                return JsonResponse({'code': 404, 'error': '请求错误'})
            if chapter_id == chapter_ids[0]:
                res = make_chapter_res(chapter_id, chapters_obj, books_obj)
            else:
                res = make_chapter_res(chapter_id, chapters_obj)
            return JsonResponse(res)
    else:
        return JsonResponse({'code': 304, 'error': '请求错误'})


def make_chapter_res(chapter_id, chapters_obj, books_obj=None):
    book = chapters_obj.book
    next_chapter = Chapter.objects.filter(id__gt=chapter_id, book=book).first()
    last_chapter = Chapter.objects.filter(id__lt=chapter_id, book=book).last()
    if next_chapter:
        next_id = next_chapter.id
    else:
        next_id = None
    if last_chapter:
        last_id = last_chapter.id
    else:
        last_id = None
    res = {'code': 200, 'data': {}}
    data = {'book_info': {}, 'chapter_info': {}}
    if books_obj != None:
        data['book_info']['img'] = str(books_obj.image)
        data['book_info']['authorId'] = books_obj.author.id
        data['book_info']['classification'] = parse_classification(books_obj.classification)
        data['book_info']['create_time'] = books_obj.create_time
        data['book_info']['word_count'] = books_obj.word_count
    data['chapter_info']['c_name'] = chapters_obj.name
    data['chapter_info']['b_name'] = chapters_obj.book.name
    data['chapter_info']['author'] = chapters_obj.book.author.name
    data['chapter_info']['authorId'] = chapters_obj.book.author.id
    data['chapter_info']['create_time'] = chapters_obj.create_time
    data['chapter_info']['word_count'] = chapters_obj.book.word_count
    data['chapter_info']['next_chapter'] = next_id
    data['chapter_info']['last_chapter'] = last_id
    contents = chapters_obj.content
    contents_list = contents.split('\n')
    data['chapter_info']['content'] = contents_list
    res['data'] = data
    return res
