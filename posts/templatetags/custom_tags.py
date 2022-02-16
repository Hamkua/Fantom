from django import template
from posts.models import Category, Tag

register = template.Library()

@register.simple_tag(name='categories')
def all_categories():
    return Category.objects.all()

@register.simple_tag(name='tags')
def all_tags():
    return Tag.objects.all()