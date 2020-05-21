from django.urls import path
from . import views

app_name="blog"
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('<int:pk>/', views.Perma.as_view(), name='onepost'),
    path('newpost/', views.NewPost.as_view(), name='newpost'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('editprofile/', views.EditProfile.as_view(), name='editprofile'),
    path('editpass/', views.EditPassword.as_view(), name='editpass'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('dataa', views.FacebookData.as_view(), name='facebookdata'),
    #path('', views.perma, name='perma'),
]