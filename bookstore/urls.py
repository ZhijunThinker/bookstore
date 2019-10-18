"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', include('index.urls')),
    url(r'^search', include('search.urls')),
    url(r'^v1/readers', include('reader.urls')),
    url(r'^v1/tokens', include('btoken.urls')),
    url(r'^chapter/', include('chapter.urls')),
    url(r'^v1/bookrack',include('bookrack.urls')),
    url(r'^v1/comment',include('comment.urls')),
    url(r'^v1/book',include('book.urls')),
]
# 生成媒体资源路由
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
