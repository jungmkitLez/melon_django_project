from django.contrib import admin
from django.urls import path, include
from django.urls.resolvers import URLPattern
from api import views

app_name = 'api'

urlpatterns = [
    # path('tag_recommend', views.api_tag_recommend, name ='tag_recommend'),
    path('singer_recommend_api', views.SingerRecommend.as_view(), name = 'singer_recommend'),
    path('tag_recommend_api', views.TagSongRecommend.as_view(), name = 'tag_recommend'),
]   