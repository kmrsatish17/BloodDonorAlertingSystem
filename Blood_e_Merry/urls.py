"""Blood_e_Merry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic import RedirectView

# from loginsignup import views
#
# # above import might not work
from Blood_e_Merry import views

urlpatterns = [
    url(r'^$', views.redirect_home, name='redirect_home'),  # actual home page
    url(r'^home/', include('loginsignup.urls')),
    url(r'^admin/', admin.site.urls),
]
