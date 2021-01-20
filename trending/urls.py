from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^panel/trending/add/$', views.tranding_add, name='tranding_add'),
    url(r'^panel/trending/del/(?P<pk>\d+)/$', views.trending_del, name='trending_del'),
    url(r'^panel/trending/edit/(?P<pk>\d+)/$', views.trending_edit, name='trending_edit'),

]
