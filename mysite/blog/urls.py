from django.urls import *
import blog.views
urlpatterns = [
    # 第一个参数是路径，第二个参数是视图函数，在调用到这个URL时用于处理信息
    path('', blog.views.archive),
    path(r'create/', blog.views.create_blogpost)
]
