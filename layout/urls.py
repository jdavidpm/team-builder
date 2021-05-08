from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='layout-index'),
    path('FAQ/', views.faq, name='layout-faq'),
    path('about/', views.about, name='layout-about'),
    path('HEXACO/', views.hexaco_test, name='layout-hexaco-test'),
    path('tools/', views.tools, name='layout-tools')
]