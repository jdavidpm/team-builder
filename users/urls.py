from django.urls import path
from django.contrib.auth import views as authViews
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import SignInFrom

urlpatterns = [
    path('notifications/service', views.notifications, name='users-notifications'),
    path('notifications/', views.notifications_list, name='users-notifications-list'),
    path('profile/<str:username>/', views.profile, name='users-profile'),
    path('signup/', views.signup, name='users-signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='users-activate'),
    path('signin/', authViews.LoginView.as_view(template_name='users/signin.html', authentication_form=SignInFrom), name='users-signin'),
    path('signout/', authViews.LogoutView.as_view(template_name='users/signout.html'), name='users-signout'),
    path('recover/', authViews.PasswordResetView.as_view(template_name='users/recover.html'), name='password_reset'),
    path('recover/done', authViews.PasswordResetDoneView.as_view(template_name='users/recover_done.html'), name='password_reset_done'),
    path('recover/confirm/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='users/recover_confirm.html'), name='password_reset_confirm'),
    path('recover/complete', authViews.PasswordResetCompleteView.as_view(template_name='users/recover_complete.html'), name='password_reset_complete'),
    path('profile/<str:username>/update/', views.update_profile, name='users-update-profile'),
    path('profile/<str:username>/update/school/', views.update_profile_school, name='users-update-profile-school')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 