from datetime import datetime

from django.db import models
# 原有的user
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 继承自django提供的原有的字段，添加实际所需要的字段
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=10, verbose_name='昵称', default='')
    birday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), default='female', max_length=10)
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # 获取用户未读的消息
    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=15, choices=(('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')), verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code + '('+self.email + ')'


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图', max_length=100)
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title








