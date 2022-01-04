from django.urls import path
from article import views

urlpatterns = [
    path('', views.article_list, name='list')
]
