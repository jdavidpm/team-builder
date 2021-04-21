from django.urls import path
from django.contrib.auth import views as authViews
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='users-profile'),
    path('signup/', views.signup, name='users-signup'),
    path('signin/', authViews.LoginView.as_view(template_name='users/signin.html'), name='users-signin'),
    path('signout/', authViews.LogoutView.as_view(template_name='users/signout.html'), name='users-signout'),
    path('profile/<str:username>/update/', views.updateProfile, name='users-update-profile'),
    path('tasks/', views.tasks, name='users-tasks')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 