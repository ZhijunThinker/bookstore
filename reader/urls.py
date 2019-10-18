from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$',views.readers),
    url(r'^/(?P<readername>[\w]{1,11})$', views.readers),
    url(r'^/(?P<readername>[\w]{1,11})/avatar$',views.readers_avatar),
]
