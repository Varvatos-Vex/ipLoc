from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='index'),
    path('multiple/', views.multiip, name='multiple'),
    path('compendium/', views.compendium, name='compendium'),
]