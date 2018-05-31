from datetime import datetime

from django.db import models
# from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='所属机构', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    teacher = models.ForeignKey(Teacher, verbose_name='教师', null=True, blank=True, on_delete=models.CASCADE)
    is_banner = models.BooleanField(default=False, verbose_name='是否为轮播图')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    # detail = UEditorField(verbose_name='课程详情', width=600, height=300,  imagePath="courses/ueditor",
    # filePath="courses/ueditor", default='')
    degree = models.CharField(max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='课程点击数')
    category = models.CharField(max_length=20, verbose_name='课程类别', default='后端开发')
    tag = models.CharField(default='', verbose_name='课程标签', max_length=10)
    you_need_know = models.CharField(max_length=300, verbose_name='课程须知', default='')
    teacher_tell = models.CharField(max_length=300, verbose_name='老师提示', default='')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()
    get_zj_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.baidu.com">跳转</a>')
    go_to.short_description = '跳转'

    def get_learn_users(self):
        # 获取学习用户
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取视频信息
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='视频名称')
    url = models.CharField(max_length=200, verbose_name='访问地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100, verbose_name='资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = verbose_name


# 轮播课程
class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True



