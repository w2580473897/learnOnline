# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/5/19 14:58'
from django.conf.urls import url, include

from .views import OrgView, AddUserView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView

app_name = 'organization'
urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>.*)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>.*)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>.*)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>.*)/$', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    # 讲师列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    # 教师详情页
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail')

]