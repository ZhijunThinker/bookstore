from django.shortcuts import render
from book.models import Book
from django.http import JsonResponse
import json
from chapter.models import Chapter
from comment.models import Comment
from tools.parse_classification import parse_classification
# Create your views here.
def book_details(request,book_id):
    if request.method == 'GET':
        books = Book.objects.filter(id=book_id)
        if not books:
            return JsonResponse({'code':404,'error':'Book_id is wrong'})
        abook = books[0]
        if abook.is_forbid:
            return JsonResponse({'code':404,'error':'The book is banned'})
        # ch = request.GET.get('ch')
        # if not ch:
        #     res = make_book_res(abook)
        #     return JsonResponse(res)
        # else:
        #     res = make_chapter_res(abook)
        #     return JsonResponse(res)
        res = make_book_res(abook)
        return JsonResponse(res)


def make_book_res(abook):
    print(abook.id)
    data = {}
    chapter_list = Chapter.objects.filter(book=abook)
    chapter_count = len(chapter_list)
    chapters = []
    for c in chapter_list:
        chapter = {}
        chapter['name'] = c.name
        chapter['cid'] = c.id
        chapters.append(chapter)
    all_comments = Comment.objects.filter(book=abook)
    comments = []
    comment_count = 0
    for c in all_comments:
        comment = {}
        comment['user_name'] = c.reader.nickname
        reader_avatar = 'http://176.209.103.9:8000/media/' + str(c.reader.avatar)
        comment['avatar'] =reader_avatar
        comment['create_time'] = c.created_time.strftime('%Y-%m-%d %H:%M:%S')
        comment['content'] = c.content
        comments.append(comment)
        comment_count += 1

    data['id'] = abook.id
    data['name'] = abook.name
    data['imageUrl'] = str(abook.image)
    data['click_volume'] = abook.click_volume
    data['introduction'] = abook.introduction
    data['authorId'] = abook.author.id
    data['authorName'] = abook.author.name
    data['authorAvatar'] = str(abook.author.avator)
    data['classification'] = parse_classification(abook.classification)
    data['is_end'] = abook.is_end
    data['collection_amount'] = abook.collection_amount
    data['word_count'] = abook.word_count
    data['comment'] = comments
    data['comment_count'] = comment_count
    data['recommend'] = get_recommend(abook.classification)
    data['chapters'] = chapters
    data['chapters_count'] = chapter_count
    try:
        lastChapter = Chapter.objects.filter(book=abook).last()
        data['lastChapterName'] = lastChapter.name
        data['lastChapterId'] = lastChapter.id
    except:
        data['lastChapterName'] = ''
        data['lastChapterId'] = ''
    res = {'code':200 , 'data':data}
    return res

def make_chapter_res(abook):
    chapter_list = Chapter.objects.filter(book=abook)
    count = len(chapter_list)
    chapters = []
    for c in chapter_list:
        chapter = {}
        chapter['name'] = c.name
        chapter['cid'] = c.id
        chapters.append(chapter)
    data = {'count': count, 'chapter': chapters}
    res = {'code':200 , 'data':data}
    return res

def get_recommend(classification):
    books = Book.objects.filter(classification=classification).order_by('collection_amount')[:5]
    res = []
    for b in books:
        book = {}
        book['id'] = b.id
        book['name'] = b.name
        book['imageUrl'] = str(b.image)
        book['introduction'] = b.introduction
        book['authorId'] = b.author.id
        book['authorName'] = b.author.name
        book['collection_amount'] = b.collection_amount
        res.append(book)
    return res
