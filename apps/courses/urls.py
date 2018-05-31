# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/5/23 15:46'
from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentView, AddCommentView, VideoPlayView

app_name = 'course'

urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),
    # 添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),

]