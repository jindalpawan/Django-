from django.urls import path
from . import views

app_name="blog"
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('newpost', views.NewPost.as_view(), name='newpost'),
    #path('', views.perma, name='perma'),
]