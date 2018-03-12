from django.shortcuts import render
from blog.models import BlogPost, BlogPostForm
from django.template import loader, Context
from django.shortcuts import render_to_response
from datetime import datetime
from django.http import HttpResponseRedirect
from django.template import RequestContext
# Create your views here.


def archive(request):
    # 在timestamp前面加上减号(-)指定按时间逆序排列。正常的升序只需要移除减号
    posts = BlogPost.objects.all()[:10]
    return render(request, 'archive.html', {'posts': posts, 'form': BlogPostForm()})


def create_blogpost(request):
    if request.method == 'POST':
        # 检查POST请求
        # 创建新的BlogPost项，获取表单数据，并用当前时间建立时间戳。
        # BlogPost(
        #     title=request.POST.get('title'),
        #     body=request.POST.get('body'),
        #     timestamp=datetime.now()
        # ).save()
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.timestamp = datetime.now()
            post.save()
    # 重定向会/blog
    return HttpResponseRedirect('/blog')
