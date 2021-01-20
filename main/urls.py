from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^login/$', views.mylogin, name='mylogin'),
    url(r'^logout/$', views.mylogout, name='mylogout'),
    url(r'^panel/site/setting/$', views.site_setting, name='site_setting'),
    url(r'^panel/about/setting/$', views.about_setting, name='about_setting'),
    url(r'^panel/change/password/$', views.change_pass, name='change_pass'),
    url(r'^panel/change/username/$', views.change_admin, name='change_admin'),
    url(r'^register/$', views.myregister, name='myregister'),
    url(r'^answer/cm/(?P<pk>\d+)/$', views.answer_cm, name='answer_cm'),
    url(r'^show/data/$', views.show_data, name='show_data'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='front/forgetpass.html'), name='password_reset'),
    url(r'^password_reset_done/$', auth_views.PasswordResetDoneView.as_view(template_name='front/forgetpass_done.html'), name='password_reset_done'),
    url(r'^password_reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(template_name='front/forgetpass_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^password_reset_complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='front/forgetpass_reset_complete.html'), name='password_reset_complete'),
    url(r'^panel/latest/article/$', views.latest_article, name='latest_article'),
    url(r'^panel/popular/article/$', views.popular_article, name='popular_article'),
    url(r'^panel/user/profile/image/$', views.users_profiles, name='users_profiles'),
]