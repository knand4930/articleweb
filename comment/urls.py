from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^comment/add/news/(?P<pk>\d+)/$', views.news_cm_add, name='news_cm_add'),
    url(r'^panel/comment/list/$', views.comments_list, name='comments_list'),
    url(r'^panel/comment/del/(?P<pk>\d+)/$', views.comments_del, name='comments_del'),
    url(r'^panel/comment/confirm/(?P<pk>\d+)/$', views.comments_confirm, name='comments_confirm'),

]