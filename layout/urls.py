from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='layout-index'),
    path('loaderio-4e678146c7228bcfb2f2028d48831e29/', views.token_load, name='token-load'),
    path('FAQ/', views.faq, name='layout-faq'),
    path('about/', views.about, name='layout-about'),
    path('HEXACO/', views.hexaco_test, name='layout-hexaco-test'),
    path('HEXACO/results/', views.hexaco_results, name='layout-hexaco-results'),
    path('HEXACO/compare/<str:username>', views.hexaco_compare, name='layout-hexaco-compare'),
    path('tools/', views.tools, name='layout-tools'),
    path('search/', views.search_results, name='layout-search-results')
]