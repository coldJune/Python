from django.db import models

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
