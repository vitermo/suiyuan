from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from .models import User

class LoginForm(forms.Form,FormMixin):
    telepone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=10,min_length=4,
    error_messages={'max_length':'密码最多不能超过10个字符','min_length':'密码最少不能低于4位'})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form,FormMixin):
    telepone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=10,min_length=4,
    error_messages={'max_length':'密码最多不能超过10个字符','min_length':'密码最少不能低于4位'})
    password2 = forms.CharField(max_length=10, min_length=4,
    error_messages={'max_length': '密码最多不能超过10个字符', 'min_length': '密码最少不能低于4位'})
    img_captcha = forms.CharField(max_length=4,min_length=4)
    sms_captcha = forms.CharField(max_length=4,min_length=4)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致！')

        img_captcha = cleaned_data.get('img_captcha')
        cache_img_captcha = cache.get(img_captcha.lower())
        if not cache_img_captcha or cache_img_captcha.lower() != \
        img_captcha.lower():
            raise forms.ValidationError('图形验证码错误！')

        telepone = cleaned_data.get('telepone')
        sms_captcha = cleaned_data.get('sms_captcha')
        cache_sms_captcha = cache.get(telepone)
        if not cache_sms_captcha or cache_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        exists = User.objects.filter(telepone=telepone).exists()
        if exists:
            raise forms.ValidationError('该手机号码已经被注册！')
        return cleaned_data


