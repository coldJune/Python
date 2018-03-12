from django.db import models
from django import forms
# Create your models here.


class BlogPost(models.Model):
    """
    django.db.models.Model的子类Model是Django中用于数据模型的标准基类。
    BlogPost中的字段像普通类属性那样定义，
    每个都是特定字段类的实例，每个实例对应数据库中的一条记录。
    """
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ('-timestamp',)


class BlogPostForm(forms.ModelForm):
    class Meta:
        # 定义一个Meta类，他表示表单基于哪个数据模型。当生成HTML表单时，会含有对应数据模型中的所有属性字段。
        # 不信赖用户输入正确的时间戳可以通过添加exclude属性来设置。
        model = BlogPost
        exclude = ('timestamp',)


