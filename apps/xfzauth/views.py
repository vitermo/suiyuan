from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from utils import restful
from django.shortcuts import redirect,reverse
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.http import HttpResponse
from utils import smssender
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()

@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telepone = form.cleaned_data.get('telepone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=telepone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message='账号被冻结')
        else:
            return restful.params_error(message='用户名或密码错误')
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)



def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telepone = form.cleaned_data.get('telepone')
        print(telepone)
        username = form.cleaned_data.get('username')
        print(username)
        password = form.cleaned_data.get('password1')
        print(password)
        user = User.objects.create_user(telepone=telepone,username=username,password=password)
        login(request,user)
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.params_error(message=form.get_errors())

def img_captcha(reauest):
    text,image = Captcha.gene_code()
    # BytesIO:相当于一个管道，用于存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中读取出图片的数据，保存在response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(),text.lower(),5*60)
    return response

def sms_captcha(request):
    telepone = request.GET.get('telepone')
    code = Captcha.gene_text()
    cache.set(telepone,code,5*60)
    print('短信验证码：',code)
    # result = smssender.send(telepone,code)
    # if result:
    return restful.ok()
    # else:
        # return restful.params_error(message='短信验证码发送失败！')


def cache_redis(request):
    cache.set('v', '1234sdajaoisdjoad56',60)  # 写入key为v，值为555的缓存，有效期30分钟
    # cache.has_key('v')  # 判断key为v是否存在
    result = cache.get('v')
    print(result)
    return HttpResponse('哈哈')

