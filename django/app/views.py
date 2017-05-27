# coding: utf-8
"""View module."""
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from core.models import Account, Topic, Space, Vote, Stat, Event

from .utils import sendemail

from uuid import uuid4 as uuid


def requirelogin(func=None):
    """Decorator for requiring login."""
    nextpage = func.__name__[:-len('view')]

    def _requirelogin(request, *args, **kwargs):
        """Local require login."""
        if isinstance(request.user, User):
            return func(request, *args, **kwargs)

        else:
            return redirect('login.html?next={0}'.format(nextpage))

    return _requirelogin


def basecontext(request, page='home', tableofcontents=False):
    """Get base context.

    :rtype: dict
    """
    spacecount = Space.objects.count()
    topiccount = Topic.objects.count()
    accountcount = Account.objects.count()
    votecount = Vote.objects.count()
    eventcount = Event.objects.count()

    result = {
        'spacecount': spacecount, 'topiccount': topiccount,
        'eventcount': eventcount,
        'votecount': votecount, 'accountcount': accountcount,
        'page': page,
        'tableofcontents': tableofcontents,
        'next': request.GET.get('next', page),
        'host': settings.HOST, 'api': settings.API,
        'DEBUG': settings.DEBUG
    }

    return result


def rendernextpage(request, context):
    """Redirect to the nextage."""
    nextpage = context.pop('next', 'home') or 'home'
    return render(request, '{0}.html'.format(nextpage), context=context)


def loginview(request):
    """Login view."""
    username = email = request.POST.get('email')

    context = basecontext(request, 'login')

    result, user = None, None

    if email is not None:
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            try:
                user = User.objects.get(email=email, username=username)

            except User.DoesNotExist:
                user = User(email=email, username=username)
                user.set_password(password)
                user.save()
                account = Account(user=user)
                account.save()

            else:
                context['errors'] = ['Mauvais mot de passe !']
                context['csrf_token'] = request.POST['csrfmiddlewaretoken']
                context['username'] = username
                context['email'] = email
                user = None

    if user is None:
        result = render(request, 'login.html', context)

    else:
        login(request, user, 'django.contrib.auth.backends.ModelBackend')
        result = redirect('/{0}'.format(request.GET.get('next', '')))

    return result


def logoutview(request):
    """Login view."""
    logout(request)
    context = basecontext(request)
    context['successes'] = ['Vous êtes déconnecté !']
    return redirect('/{0}'.format(request.GET.get('next', '')))


def resetpwdview(request):
    """Reset password view."""
    result = None

    lost_key = request.GET.get('lost_key', request.POST.get('lost_key'))

    context = basecontext(request, 'resetpwd')

    if lost_key is None:
        result = render(request, 'resetpwd.html', context=context)

    else:
        context['lost_key'] = lost_key

        email = request.GET.get('email', request.POST.get('email'))
        if email is None:
            context['errors'] = ['Email manquant !']
            context['page'] = 'home'
            result = render(request, 'home.html', context=context)

        else:
            context['email'] = email

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                context['errors'] = [
                    'Email {0} non enregistré !'.format(email)
                ]
                context['page'] = 'home'
                result = render(request, 'home.html', context=context)

            else:
                account = user.account
                password = request.POST.get('password')

                if 'email' in request.GET:
                    result = render(request, 'resetpwd.html', context=context)

                elif password is None:
                    lost_key = str(uuid())
                    account.lost_key = lost_key
                    account.save()

                    url = '{0}/resetpwd?lost_key={1}&email={2}'.format(
                        settings.HOST, lost_key, email
                    )
                    subject = 'Réinitialiser le mot de passe de lechangement'
                    msg = 'Réinitialiser le mot de passe de : {0}'.format(url)
                    html = '<a href="{0}">Changer mot de passe !</a>'.format(
                        url
                    )
                    sendemail(subject, msg, html, email)

                    context['successes'] = [
                        'Changement de mot de passe envoyé !'.format(email)
                    ]
                    result = render(request, 'resetpwd.html', context=context)

                else:
                    context['lost_key'] = lost_key

                    if 'lost_key' in request.POST:  # reset password
                        password = request.POST['password']

                        account.user.set_password(password)
                        account.lost_key = None
                        account.save()
                        account.user.save()
                        login(
                            request, user,
                            'django.contrib.auth.backends.ModelBackend'
                        )

                        context['successes'] = ['Mot de passe changé !']
                        context['page'] = 'home'
                        result = rendernextpage(request, context=context)

                    elif 'lost_key' in request.GET:  # reset form
                        result = render(
                            request, 'resetpwd.html', context=context
                        )

    return result


def getuserid(request):
    """Get user id from input request.

    If user is authenticated, get user id. Otherwise, get
    request.COOKIES.get('userid', uuid()).
    """
    if request.user.is_authenticated():
        result = request.user.id

    else:
        result = request.COOKIES.get('userid', uuid())

    return result


def appcontext(request, page='home', tableofcontents=False):
    """Get app context.

    :rtype: dict
    """
    result = basecontext(request, page, tableofcontents)

    result['admins'] = [Account.objects.filter(administrated__isnull=False)]

    if page[-1] == 's':
        result['type'] = page[:-1]

    return result


def searchview(request, model):
    """Search view."""
    page = '{0}s'.format(model.__name__.lower())
    context = appcontext(request, page=page, tableofcontents=True)
    return render(request, 'search.html', context=context)


def spacesview(request):
    """View of spaces."""
    return searchview(request, Space)


def eventsview(request):
    """View of events."""
    return searchview(request, Event)


def topicsview(request):
    """View of Topics."""
    return searchview(request, Topic)


def votesview(request):
    """View of votes."""
    context = appcontext(request, page='votes', tableofcontents=True)
    return render(request, 'search.html', context=context)


def accountsview(request):
    """View of accounts."""
    context = appcontext(request, page='accounts', tableofcontents=True)
    return render(request, 'search.html', context=context)


@requirelogin
def accountview(request):
    """Account view."""
    context = appcontext(request, 'account', True)
    return render(request, 'account.html', context=context)


def homeview(request):
    """Home view."""
    context = basecontext(request, 'home')
    return render(request, 'home.html', context=context)


@requirelogin
def topicview(request):
    """Topic view."""
    return editview(request, 'topic')


@requirelogin
def eventview(request):
    """Event view."""
    return editview(request, 'event')


@requirelogin
def spaceview(request):
    """Space view."""
    return editview(request, 'space')


def editview(request, page):
    """Edit space/topic."""
    context = appcontext(
        request, page=page, tableofcontents=False
    )

    if 'id' not in request.POST:
        instance = globals()[page.title()]()

    else:
        instance = globals()[page.title()].objects.get(id=request.POST['id'])

    def filldefaults(*names):
        """Fill defaults."""
        for name in names:
            if name in request.POST:
                val = request.POST[name]
                setattr(instance, name, val)

    if page == 'comment':
        filldefaults('content', 'cited')

    else:
        filldefaults('name', 'description', 'public')

        admins = request.POST.get('admins', '')
        admins = admins.split(',') if admins else []
        if request.user.id not in admins:
            admins.append(request.user.id)
        instance.save()
        instance.admins.set(admins)

        if page == 'space':
            filldefaults('address', 'lon', 'lat')

    instance.save()

    page = request.POST.get('next', 'search')

    return render(request, 'edit.html', context=context)


def faqview(request):
    """Faq view."""
    context = basecontext(request, 'faq')
    return render(request, 'faq.html', context=context)


def aboutview(request):
    """About view."""
    context = basecontext(request, 'about', True)
    return render(request, 'about.html', context=context)


def statsview(request):
    """Stat view."""
    context = basecontext(request, 'stats', True)
    context['stats'] = Stat.objects.all()
    context['eventcount'] = Event.objects.count()
    context['usercount'] = Account.objects.filter(uses=None).count()
    return render(request, 'stats.html', context=context)


def mytopicsview(request):
    """My Topics view."""
    context = appcontext(request, 'mytopics')
    return render(request, 'mysearch.html', context=context)


def myvotesview(request):
    """My votes view."""
    context = appcontext(request, 'myvotes')
    return render(request, 'mysearch.html', context=context)


def myspacesview(request):
    """My spaces view."""
    context = appcontext(request, 'myspaces')
    return render(request, 'mysearch.html', context=context)


def myeventsview(request):
    """My events view."""
    context = appcontext(request, 'myevents')
    return render(request, 'mysearch.html', context=context)


def mycommentsview(request):
    """My comments view."""
    context = appcontext(request, 'mycomments')
    return render(request, 'mysearch.html', context=context)


def mystatsview(request):
    """Stat view."""
    context = basecontext(request, 'stats', True)
    context['stats'] = Stat.objects.all()
    context['eventcount'] = Event.objects.count()
    context['usercount'] = Account.objects.filter(uses=None).count()
    return render(request, 'stats.html', context=context)
