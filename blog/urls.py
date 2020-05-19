from django.urls import path
from . import views

app_name="blog"
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('<int:pk>/', views.Perma.as_view(), name='onepost'),
    path('newpost/', views.NewPost.as_view(), name='newpost'),
    path('signup/', views.Signup.as_view(), name='signup'),
    #path('', views.perma, name='perma'),
]