from PIL import Image
from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify


class UserProfile(models.Model):

    # why onetoonefield? because one user only can have one field
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_day = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True)

    # imagefield에도 default 값을 줄 수 있군
    image = models.ImageField(blank=True, null=True, default='users/author.png', upload_to='users')
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


        #이미지 크기를 조정하는 방법
        img = Image.open(self.image.path)
        if img.height > 200 or img.width >200:
            new_size = (200, 200)
            img.thumbnail(new_size)
            img.save(self.image.path)


    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)