from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Blog(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_author')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='blog_category')
    title = models.CharField(max_length=250)
    description = models.TextField()
    tags = models.CharField(max_length=100) # basically I used comma separated value for tags or keywords
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)