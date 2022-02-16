from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(editable=False)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.all().count()
        # return self.post_set.all().count() foreignkey 에서는 안되는 건가?

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')    #uploads 폴더를 만들지 않아도 django가 자동적으로 생성함.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(default="slug", editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='posts')    # 1 means category id.

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title