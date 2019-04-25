from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models


class UserManage(BaseUserManager):
    def _create_user(self,telepone,username,password,**kwargs):
        if not telepone:
            raise ValueError('请输入手机号码')
        if not username:
            raise ValueError('请输入用户名')
        if not password:
            raise ValueError('请输入密码')
        user = self.model(telepone=telepone,username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_user(self,telepone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telepone,username,password,**kwargs)


    def create_superuser(self,telepone,username,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telepone,username,password,**kwargs)


class User(AbstractBaseUser,PermissionsMixin):

    uid = ShortUUIDField(primary_key=True)
    telepone = models.CharField(max_length=11,unique=True)
    email = models.EmailField(unique=True,null=True)
    username = models.CharField(max_length=100)
    #是否是可用的
    is_active = models.BooleanField(default=True)
    #是否是员工
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)



    USERNAME_FIELD = 'telepone'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManage()
    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username