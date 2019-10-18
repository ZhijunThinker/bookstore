from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<book_id>[\w]{1,11})/(?P<chapter_id>[\w]{1,11})$', views.chapter),
]
