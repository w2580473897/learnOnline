# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/5/28 18:38'

from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

app_name = 'users'
urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'^image/upload', UploadImageView.as_view(), name='upload_image'),
    # 用户中心修改密码
    url(r'^update/pwd', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),
    # 课程机构收藏
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 课程讲师收藏
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 课程收藏
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    # 我的消息
    url(r'^my_message/$', MyMessageView.as_view(), name='my_message'),
]