from django.http import JsonResponse
from django.shortcuts import render
from chapter.models import Chapter
from django.db.models import Count, Q

# Create your views here.

from book.models import Book
from tools.parse_classification import parse_classification


def do_search(request):
    if request.method == 'GET':
        kw = request.GET.get('kw', '')
        author_id = request.GET.get('authorId')
        classification = request.GET.get('classification', '')
        is_end = request.GET.get('isEnd', '')
        order_by = request.GET.get('orderBy', 'collection_amount')
        page = request.GET.get('page', 0)
        if kw:
            count = get_count('select count(id) from book where name like "%%{}%%"'.format(kw))
            books = make_res(
                'select * from book where name like "%%{}%%" order by {} limit {},10'.format(kw, order_by, page * 10))
            return JsonResponse({'code': 200, 'count': count, 'books': books})
        elif classification:
            try:
                classification = int(classification)
            except:
                return JsonResponse({'code': 404, 'error': 'not found'})
            count = get_count('select count(*) from book where classification ={}'.format(classification))
            books = make_res(
                'select * from book where classification ={} order by {} limit {},10'.format(classification, order_by,
                                                                                             page * 10))
            return JsonResponse({'code': 200, 'count': count, 'books': books})
        elif is_end == 'true' or is_end == 'false':
            count = get_count('select count(*) from book where is_end={}'.format(is_end))
            books = make_res(
                'select * from book where is_end={} order by {} limit {},10'.format(is_end, order_by, page * 10))
            return JsonResponse({'code': 200, 'count': count, 'books': books})

        else:
            return JsonResponse({'code': 404, 'error': 'not found'})
    else:
        return JsonResponse({'code': 404, 'error': '请求错误'})


def get_count(sql):
    count = Book.objects.extra(select={'count': sql})
    return count.count()


def make_res(sql):
    books = Book.objects.raw(sql)
    if books:
        res = []
        for book in books:
            b = {}
            b['name'] = book.name
            b['authorName'] = book.author.name
            b['authorId'] = book.author.id
            b['classification'] = parse_classification(book.classification)
            b['is_end'] = book.is_end
            b['introduction'] = book.introduction
            try:
                lastChapter = Chapter.objects.filter(book=book).last()
                b['lastChapterName'] = lastChapter.name
                b['lastChapterId'] = lastChapter.id
                b['lastUpdateTime'] = lastChapter.create_time
            except:
                b['lastChapterName'] = ''
                b['lastChapterId'] = ''
                b['lastUpdateTime'] = ''
            b['recommend'] = book.collection_amount
            b['wordCount'] = book.word_count
            b['imageUrl'] = str(book.image)
            b['id'] = book.id
            res.append(b)
    else:
        res = 'not found'
    return res
