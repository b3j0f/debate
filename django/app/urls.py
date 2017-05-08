# coding: utf-8
"""Debate URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin

from django.shortcuts import render

from rest_framework.routers import DefaultRouter

from .views import (
    homeview, aboutview, loginview, logoutview, resetpwdview, editview,
    accountview, accountsview, organizationsview, faqview, debatesview,
    searchview, statsview, votesview, mydebatesview, myorganizationsview,
    myvotesview, mystatsview
)

from debate.views import (
    CategoryViewSet, AccountViewSet, UserViewSet, DebateViewSet,
    MediaViewSet, SchedulingViewSet, OrganizationViewSet, VoteViewSet,
    StatViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'debates', DebateViewSet)
router.register(r'medias', MediaViewSet)
router.register(r'schedulings', SchedulingViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'stats', StatViewSet)

urlpatterns = [
    url(
        r'^{0}/auth/'.format(settings.API),
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^auth/', include('django.contrib.auth.urls'), name='auth'),
    url(r'^{0}/'.format(settings.API), include(router.urls), name='api'),
    url(r'^$', homeview),
    url(r'^home$', homeview),
    url(r'^faq', faqview),
    url(r'^about', aboutview),
    url(r'^login', loginview),
    url(r'^logout', logoutview),
    url(r'^resetpwd', resetpwdview),
    url(r'^accounts', accountsview),
    url(r'^account', accountview),
    url(r'^organizations', organizationsview),
    url(r'^debates', debatesview),
    url(r'^votes', votesview),
    url(r'^stats', statsview),
    url(r'^myorganizations', myorganizationsview),
    url(r'^mydebates', mydebatesview),
    url(r'^myvotes', myvotesview),
    url(r'^mystats', mystatsview),
    url(r'^edit', editview),
    url(r'^search', searchview),
    url('test', lambda request: render(request, 'test.html'))
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
