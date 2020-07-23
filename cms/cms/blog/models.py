from django.db import models
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.utils import timezone
#from account.models import Profile
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = "p")

class CatProgManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category__name = "DevOps")


class Post(models.Model):
    statues=[("D","Draft"),("p","published")]
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=1,choices=statues,default="D")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog/", blank = True)
    slug = models.SlugField(blank=True, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    published = PublishedPostManager()
    prog = CatProgManager()
         
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("post-details", args=[self.slug])