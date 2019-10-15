"""lifebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import add_profile_info,change_password, terms_and_privacy, team
from posts.views import (
    home, login_request,logout_request,
    register,add_post,post_likes,comment_view,comment_remove, user_profile_view
    )
from posts.views import (
    VideoCreateView, ImageCreateView, 
    PostUpdateView,PostDeleteView,
    CommentUpdateView, #CommentDeleteView
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('post/<int:id>/', comment_view, name='post'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('register/', register, name='register'),
    path('add-post/', add_post, name='add-post'),
    path('add-video/', VideoCreateView.as_view(), name='add-video'),
    path('add-photo/', ImageCreateView.as_view(), name='add-photo'),
    path('update-post/<int:pk>/', PostUpdateView.as_view(), name='update-post'),
    path('delete-post/<int:pk>/', PostDeleteView.as_view(), name='delete-post'),
    path('change-comment/<int:pk>/', CommentUpdateView.as_view(), name='change-comment'),
    path('delete-comment/<int:id>/', comment_remove, name='delete-comment'),
    path('add-info/', add_profile_info, name='add-info'),
    path('profile-info/<int:id>', user_profile_view, name='profile-info'),
    path('privacy-policy/', terms_and_privacy, name='privacy-policy'),
    path('team/', team, name='team'),

    path('likes/',post_likes, name='likes'),
    path('password-change/', change_password, name='password-change'),
    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='posts/password_reset.html'),name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name='posts/password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='posts/password_reset_confirm.html'),name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='posts/password_reset_complete.html'), name="password_reset_complete"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
