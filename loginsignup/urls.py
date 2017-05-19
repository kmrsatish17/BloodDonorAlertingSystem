from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

app_name = 'loginsignup'
urlpatterns = [
    # ex: /home/
    url(r'^$', views.home, name='home'),
    # ex: /home/signup/
    url(r'^signup/$', views.signup, name='signup'),
    # ex: /home/confirmation/
    url(r'^confirmation/$', views.confirmation, name='confirmation'),
    # ex: /home/login/
    url(r'^login/$', login, {'template_name': 'loginsignup/login.html'}, name='login'),
    # ex: /home/profile/
    url(r'^profile/$', views.profile, name='profile'),
    # ex: /home/logout/
    url(r'^logout/$', logout, {'template_name': 'loginsignup/logout.html'}, name='logout'),
    # ex: /home/profile/edit/
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    # ex: /home/change-password/
    url(r'^change-password/$', views.change_password, name='change_password'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
