# login_check('PUT','GET','POST')
import jwt
from django.http import JsonResponse
from reader.models import Reader_Profile

KEY = '1234567'


def login_check(*methods):
    def _login_check(func):
        def wrapper(request, *args, **kwargs):
            token = request.META.get('HTTP_AUTHORIZATION')
            if request.method not in methods:
                return func(request, *args, **kwargs)
            if not token:
                result = {'code': 107, 'error': 'Please login'}
                return JsonResponse(result)
            try:
                res = jwt.decode(token, KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                # token过期了
                result = {'code': 108, 'error': 'Please login'}
                return JsonResponse(result)
            except Exception as e:
                result = {'code': 109, 'error': 'Please login'}
                return JsonResponse(result)

            readername = res['readername']
            try:
                user = Reader_Profile.objects.get(readername=readername)
            except:
                user = None
            if not user:
                result = {'code': 110, 'error': 'no user'}
                return JsonResponse(result)
            # 将查询成功的user赋值给request,相当于给request对象赋予了一个属性
            request.user = user
            return func(request, *args, **kwargs)

        return wrapper

    return _login_check


def get_user_by_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        res = jwt.decode(token, KEY)
    except:
        return None
    readername = res['readername']
    try:
        user = Reader_Profile.objects.get(readername=readername)
    except:
        return None
    return user
