# coding: utf-8
"""knowledge sharing URL Configuration.

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
    homeview, aboutview, loginview, logoutview, resetpwdview, accountview,
    accountsview, spacesview, faqview, topicsview, statsview, votesview,
    mytopicsview, myspacesview, myvotesview, mystatsview, eventview,
    mycommentsview, eventsview, myeventsview, topicview, spaceview,
)

from core.views import (
    TagViewSet, AccountViewSet, UserViewSet, TopicViewSet, StatViewSet,
    MediaViewSet, EventViewSet, SpaceViewSet, VoteViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'tags', TagViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'medias', MediaViewSet)
router.register(r'events', EventViewSet)
router.register(r'spaces', SpaceViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'stats', StatViewSet)

urlpatterns = [
    # API
    url(
        r'^{0}/auth/'.format(settings.API),
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^auth/', include('django.contrib.auth.urls'), name='auth'),
    url(r'^{0}/'.format(settings.API), include(router.urls), name='api'),
    # basic pages
    url(r'^$', homeview),
    url(r'^home', homeview),
    url(r'^faq', faqview),
    url(r'^about', aboutview),
    url(r'^stats', statsview),
    # login
    url(r'^login', loginview),
    url(r'^logout', logoutview),
    url(r'^resetpwd', resetpwdview),
    # search
    url(r'^accounts', accountsview),
    url(r'^spaces', spacesview),
    url(r'^events', eventsview),
    url(r'^topics', topicsview),
    url(r'^votes', votesview),
    # account instances
    url(r'^myspaces', myspacesview),
    url(r'^myevents', myeventsview),
    url(r'^mytopics', mytopicsview),
    url(r'^myvotes', myvotesview),
    url(r'^mycomments', mycommentsview),
    url(r'^mystats', mystatsview),
    # single instance
    url(r'^account', accountview),
    url(r'^space', spaceview),
    url(r'^topic', topicview),
    url(r'^event', eventview),
    # static & media content
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(
        url('test', lambda request: render(request, 'test.html'))
    )
