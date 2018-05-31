# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2018/5/14 10:15'

import xadmin
from xadmin import views


from .models import EmailVerifyRecord, Banner, UserProfile


class BaseSetting(object):
    # 主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 左上角的文字内容
    site_title = '在线学习后台管理系统'
    # 底部文字内容
    site_footer = '在线学习网'
    # 将左侧导航栏的内容收起来
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-camera-retro'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
