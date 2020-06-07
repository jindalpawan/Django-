from django.urls import path
from . import views

app_name="blog"
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('post/<int:pk>/', views.Perma.as_view(), name='onepost'),
    path('post/delete/<int:pk>/', views.PostDelete.as_view(), name='deletepost'),
    path('post/newpost/', views.NewPost.as_view(), name='newpost'),
    path('post/comment/', views.comments, name='cmnt'),
    path('post/comments/', views.AllComments, name='cmntes'),
    path('post/like/', views.PostLike, name='like'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('user/editprofile/', views.EditProfile.as_view(), name='editprofile'),
    path('user/editpass/', views.EditPassword.as_view(), name='editpass'),
    path('user/profile/', views.Profile.as_view(), name='profile'),
    path('dataa', views.FacebookData.as_view(), name='facebookdata'),
    
]