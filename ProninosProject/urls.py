"""ProninosProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from ProninosProject.views import Home


urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^friends/', include('ProninosProject.friends.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^Auth/', include('ProninosProject.Auth.urls')),
    url(r'^contributions/', include('ProninosProject.contributions.urls')),
    url(r'^projects/', include('ProninosProject.projects.urls')),
    url(r'^events/', include('ProninosProject.events.urls')),
    url(r'^campaigns/', include('ProninosProject.campaigns.urls')),
    url(r'^billing/', include('ProninosProject.billing.urls')),
    url(r'^reports/', include('ProninosProject.reports.urls')),
    url(r'^zip/', include('ProninosProject.zip_codes.urls')),
]

