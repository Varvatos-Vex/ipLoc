"""ThreatReputation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from ThreatReputation import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from filebrowser.sites import site

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('', include('iprep.urls')),
    path('accounts/', include('account.urls')),
]

'''handler400 = 'ThreatReputation.views.bad_request'
handler403 = 'ThreatReputation.views.permission_denied'
handler404 = 'ThreatReputation.views.page_not_found'
handler500 = 'ThreatReputation.views.server_error' '''