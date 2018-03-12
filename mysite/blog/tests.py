from django.test import TestCase
from datetime import datetime
from django.test.client import Client
from blog.models import BlogPost
# Create your tests here.


class BlogPostTest(TestCase):
    # 测试方法必须以“test_”开头，方法名后面的部分随意。
    def test_obj_create(self):
        # 这里仅仅通过测试确保对象成功创建，并验证标题内容
        BlogPost.objects.create(
            title='raw title', body='raw body', timestamp=datetime.now())
        # 如果两个参数相等则测试成功，否则该测试失败
        # 这里验证对象的数目和标题
        self.assertEqual(1, BlogPost.objects.count())
        self.assertEqual('raw title', BlogPost.objects.get(id=1).title)

    def test_home(self):
        # 在'/blog/'中调用应用的主页面，确保收到200这个HTTP返回码
        response = self.client.get('/blog/')
        self.assertIn(response.status_code, (200, ))

    def test_slash(self):
        # 测试确认重定向
        response = self.client.get('/')
        self.assertIn(response.status_code, (301, 302))

    def test_empty_create(self):
        # 测试'/blog/create/'生成的视图，测试在没有任何数据就错误地生成GET请求，
        # 代码应该忽略掉这个请求，然后重定向到'/blog'
        response = self.client.get('/blog/create/')
        self.assertIn(response.status_code, (301, 302))

    def test_post_create(self):
        # 模拟真实用户请求通过POST发送真实数据，创建博客项，让后将用户重定向到"/blog"
        response = self.client.post('/blog/create/', {
            'title': 'post title',
            'body': 'post body'
        })
        self.assertIn(response.status_code, (301, 302))
        self.assertEqual(1, BlogPost.objects.count())
        self.assertEqual('post title', BlogPost.objects.get(id=1).title)
