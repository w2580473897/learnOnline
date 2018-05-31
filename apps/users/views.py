from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic.base import View
from django.shortcuts import render_to_response
# 对密码进行加密
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
import json

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course

# Create your views here.


# 重写验证方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse('index'))


# 登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_wd = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_wd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.urls import reverse
                    return HttpResponseRedirect(reverse('index'))

                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                for i in UserProfile.objects.all():
                    if user_name not in str(i):
                        return render(request, 'login.html', {'msg': '用户不存在！'})
                    else:
                        return render(request, 'login.html', {'msg': '用户名或者密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': '用户已经存在!', 'register_form': register_form})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对明文密码进行加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册在线学习网'
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 激活用户
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


# 找回密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


# 修改用户密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


# 用户个人信息
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'info'
        return render(request, 'usercenter-info.html', {
            'current_page': current_page,
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')


# 在个人中心修改密码
class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '两次密码不一致'}), content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# 发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps({'email': '邮箱已经存在'}), content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')


# 修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')

        else:
            return HttpResponse(json.dumps({'email': '验证码出错'}), content_type='application/json')


# 用户课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'course'
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
            'current_page': current_page,
        })


# 用户课程机构收藏
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav'
        flag = 'org'
        orgList = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            orgList.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'orgList': orgList,
            'flag': flag,
            'current_page': current_page,
        })


# 用户课程讲师收藏
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav'
        flag = 'teacher'
        teacherList = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacherList.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacherList': teacherList,
            'flag': flag,
            'current_page': current_page
        })


# 用户课程讲师收藏
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav'
        courseList = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            courseList.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'courseList': courseList,
            'current_page': current_page

        })


# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'message'
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, request=request, per_page=2)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'all_messages': messages,
            'current_page': current_page,
        })


# 首页
class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


# 404页面
def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 500页面
def page_error(request):
    response = render_to_response('404.html', {})
    response.status_code = 500
    return response


# # sql注入不安全的登录
# class LoginUnsafeView(View):
#     def get(self, request):
#         return render(request, 'login.html')
#
#     def post(self, request):
#         user_name = request.POST.get('username', '')
#         pass_wd = request.POST.get('password', '')
#         import pymysql
#         conn = pymysql.connect('localhost', 'root', '123456', 'learnOnline')
#         cursor = conn.cursor()
#         sql_select = 'select * from users_userprofile WHERE email={0}AND password={1}'.format(user_name, pass_wd)
#         result = cursor.execute(sql_select)
#         for row in cursor.fetchall():
#             pass

















