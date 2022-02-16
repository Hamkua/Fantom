from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/<int:pk>/<slug:slug>/', PostDetail.as_view(), name='detail'),
    path('category/<int:pk>/<slug:slug>/', CategoryDetail.as_view(), name='category_detail'),
]
