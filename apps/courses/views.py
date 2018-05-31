from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


# 课程列表页
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))

        # 热门和参与人数进行排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, request=request, per_page=6)
        courses = p.page(page)
        return render(request, 'course_list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)

        else:
            relate_courses = ''
        return render(request, 'course_detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


# 课程视频信息
class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否关联课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取所有的课程id
        course_ids = [user_courser.course.id for user_courser in all_user_courses]
        # 获取学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course_video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,

        })


# 课程评论
class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.all()
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取所有的课程id
        course_ids = [user_courser.course.id for user_courser in all_user_courses]
        # 获取学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course_comment.html', {
            'course': course,
            'all_comments': all_comments,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })


# 添加课程评论
class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            resp = {'status': 'fail', 'msg': '用户未登录'}
            return HttpResponse(json.dumps(resp), content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.course = course
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')


# 视频播放
class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否关联课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取所有的课程id
        course_ids = [user_courser.course.id for user_courser in all_user_courses]
        # 获取学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course_play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video,

        })


