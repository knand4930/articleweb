from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^news/(?P<word>.*)/$', views.news_details, name='news_details'),
    url(r'^panel/article/list/$', views.news_list, name='news_list'),
    url(r'^panel/article/add/$', views.news_add, name='news_add'),
    url(r'^panel/news/delete/(?P<pk>\d+)/$', views.news_delete, name='news_delete'),
    url(r'^panel/article/edit/(?P<pk>\d+)/$', views.article_edit, name='article_edit'),
    url(r'^panel/news/publish/(?P<pk>\d+)/$', views.news_publish, name='news_publish'),
    url(r'^urls/(?P<pk>\d+)/$', views.news_details_short, name='news_details_short'),
    url(r'^all/news/(?P<word>.*)/$', views.news_all_show, name='news_all_show'),
    url(r'^top/news/all/$', views.all_news, name='all_news'),
    url(r'^search/$', views.all_news_search, name='all_news_search'),
    url(r'^panel/advanced/search/$', views.bot_search, name='bot_search'),

]

