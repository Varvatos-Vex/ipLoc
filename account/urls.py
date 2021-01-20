from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('', views.home_view, name='accounts'),
    path('ingestion/', views.ingestion, name='ingestion'),
    path('services/', views.service, name='service'), #------------use for unbuntu services
    path('FileServe/', views.fileserver, name='fileserver'), #------------use for File Service
    path('Download/', views.download, name='download'), #------------use for File Service
]