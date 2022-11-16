from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',home, name='home'),
    path('login/',login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('add-blog/', add_blog, name= 'add_blog'),
    path('blog-detail/<slug>/', blog_detail, name='blog_detail'),
    path('see-blog/', see_blog , name='see_blog'),
    path('blog-delete/<id>/', blog_delete, name='blog_delete'),
    path('update-blog/<slug>/', blog_update, name='blog_update'),
    path('logout_view/', logout_view, name='logout_view'),
    path('verify/<token>/', verify, name='verify'),
    
# reset password

    # url name is fixed (taken from django docs)

    path('reset-password/',auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password-sent/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # uidb64: The user’s id encoded in base 64.
    # token: Token to check that the password is valid.

    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
