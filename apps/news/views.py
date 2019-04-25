from django.shortcuts import render
from .models import News,NewsCategory,Banner
from django.conf import settings
from utils import restful
from django.http import Http404
from .serializers import NewsSerializers,CommentSerializers
from .forms import PublicCommentForm
from .models import Comment
from apps.xfzauth.decorators import xfz_login_require


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category', 'author').all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses':newses,
        'categories':categories,
        'banners':Banner.objects.all(),
    }
    return render(request,'news/index.html',context=context)

def news_list(request):
    # 通过p参数来指定获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/？p=2
    page = int(request.GET.get('p',1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id',0))
    # 0,1
    # 2,3
    # 4,5
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.select_related('category','author').filter(category__id = category_id)[start:end]
    serializers = NewsSerializers(newses,many=True)
    data = serializers.data
    return restful.result(data=data)


def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category','author').prefetch_related('comments__author').get(pk=news_id)
        content = {
            'news':news,
        }
        return render(request,'news/news_detail.html',context=content)
    except News.DoesNotExist:
        raise Http404
@xfz_login_require
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serializers = CommentSerializers(comment)
        return restful.result(data=serializers.data)
    else:
        return restful.params_error(message=form.get_errors())

def search(request):
    return render(request,'search/search.html')