from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.getBooks),
    url(r'^getBook$',views.getBook),
]