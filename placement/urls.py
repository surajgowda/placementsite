"""
URL configuration for placement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static 
from django.conf import settings
from display import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/', views.companies, name='companies'),
    path('company/<int:pk>/', views.company, name='company'),
    path('',views.placement, name='placement'),
    path('about/',views.about, name='about'),
    path('login/',views.login_view, name='Login'),
    path('register/',views.register, name='Register'),
    path('dashboard/',views.home, name='MyAccount'),
    path('update/<int:user_id>/',views.update_companies_applied, name='updatecompanies'),
    path('notifications/',views.notifications, name='notifications'),
    path('logout/',views.logout_view, name='logout'),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)