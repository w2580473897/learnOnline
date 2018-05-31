"""LearnOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from LearnOnline.settings import MEDIA_ROOT
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, IndexView
from organization.views import OrgView
import users

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    # url(r'^login/$', LoginUnsafeView.as_view(), name='login'),
    # 退出
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='userActive'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构url配置

    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程相关url配置
    url(r'^course/', include('courses.urls', namespace='course')),

    # 配置上传图片访问处理
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # # 配置静态文件处理
    # url(r'^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),

    # 配置个人中心
    url(r'^users/', include('users.urls', namespace='users')),
    # 配置富文本相关url
    # url(r'^ueditor/', include('DjangoUeditor.urls')),

]
# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
