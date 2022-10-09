from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signUp,name="signup"),
    path('signin',views.signIn,name="signin"),
    path('logout',views.logOut,name="logout"),
    path('settings',views.settings,name="settings"),
    path('follow',views.follow,name="follow"),
    path('upload',views.upload,name="upload"),
    path('like-post',views.like_post,name="like-post"),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('search',views.search,name='search'),
]