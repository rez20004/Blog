#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Joanna667'


from models import Article, Tag, UserActivation
from forms import LoginForm, ArticleForm, RegistrationForm
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
import random, string
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views.decorators.cache import cache_page


def log_in(request):
    if request.user.is_authenticated():
        return index(request)

    if request.method == "GET":
        form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                if user.is_active:
                    login(request, user)
                    return index(request, 'Udało się zalogować.')
                else:
                    return index(request, 'Żeby się zalogować musisz aktywować konto!')
            else:
                message = 'Niewłaściwy login i hasło.'
    return render_to_response('login.html', locals(), RequestContext(request))


def log_out(request):
    if request.user.is_authenticated():
        logout(request)
        return index(request, 'Wylogowano!')
    return index(request)


def index(request, message=''):
    lista = Article.objects.order_by('-pub_date')
    return render_to_response('index.html', locals(), RequestContext(request))

@cache_page(60*15)
def tagged(request, idd):
    tag = Tag.objects.filter(pk=idd)
    if not tag:
        raise Http404()
    tag = tag[0]
    archive = tag.articles.all().order_by('-pub_date')
    return render_to_response("tagged.html", locals(), RequestContext(request))


def edit(request, idd):
    if not request.user.is_authenticated():
        return index(request, 'Tylko dla zalogowanych')

    art = Article.objects.all().filter(pk=idd)
    if not art:
        raise Http404()

    art = art[0]

    editable = False
    if art.mod_date:
        editable = (timezone.now() - art.mod_date).seconds < 600
    else:
        editable = (timezone.now() - art.pub_date).seconds < 600

    if (request.user.groups.filter(name='moderator')) or (editable and art.pub_user_id == request.user.id):
        if request.method == "POST":
            form = ArticleForm(request.POST)
            if form.is_valid():
                art.tytul = form.cleaned_data['tytul']
                art.mod_date = timezone.now()
                art.mod_user = request.user
                art.tresc = form.cleaned_data['tresc']
                art.tag_set.clear()
                for tag in form.cleaned_data['tags']:
                    art.tag_set.add(tag)
                art.save()
                return index(request, 'Wpis został zmodyfikowany')
        else:
            form = ArticleForm(initial={
                'tytul': art.tytul,
                'tresc': art.tresc,
                'tags': art.tag_set.all
            })
        return render_to_response("edit.html", locals(), RequestContext(request))
    else:
        return index(request, 'Nie możesz edytować!')


def create(request):
    if not request.user.is_authenticated():
        return index(request, 'Tylko dla zalogowanych')

    if request.method == "GET":
        form = ArticleForm()

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            art = Article(tytul=form.cleaned_data['tytul'],
                        tresc=form.cleaned_data['tresc'],
                        pub_user=request.user,
                        pub_date=timezone.now(),
            )
            art.save()
            for tag in form.cleaned_data['tags']:
                art.tag_set.add(tag)
            art.save()
            return index(request, 'Wpis został dodany!')

    return render_to_response('create.html', locals(), RequestContext(request))


def register(request):
    if request.user.is_authenticated():
        return index(request, 'Jesteś zalogowany, jeśli chcesz aktywować inne konto, najpierw się wyloguj')

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.is_active = False
            user.save()
            activation = UserActivation()
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
            activation.activation_key = key
            activation.user = user
            activation.save()
            #send_mail('Email aktywacyjny', 'http://myblog-joanna667.rhcloud.com/blog/users/activate/%s' % activation.activation_key, 'kotka5351@gmail.com', [user.email])
            #return index(request, 'Poczekaj kilka minut na aktywację przez administratora')
            return redirect("activate", key=key)
    else:
        form = RegistrationForm()
    return render_to_response("register.html", locals(), RequestContext(request))


def activate(request, key):
    if request.user.is_authenticated():
        return index(request, 'Jesteś zalogowany, jeśli chcesz aktywować inne konto, najpierw się wyloguj')
    activation = UserActivation.objects.all().filter(activation_key=key)[0]
    if activation:
        to_user = User.objects.all().filter(id=activation.user.id)[0]
        to_user.is_active = True
        to_user.save()
        activation.delete()
        return index(request, 'Możesz sie zalogować.')
    raise Http404()

@cache_page(60*15)
def user_posts(request, idd):
    pub_user = User.objects.all().filter(id=idd)
    if pub_user:
        pub_user = pub_user[0]
        archive = Article.objects.all().filter(pub_user_id=idd).order_by('-pub_date')
        return render_to_response('user.html', locals(), RequestContext(request))
    raise Http404()


def notfound(request):
    info = 'Nie znaleziono strony'
    return render_to_response('notfound.html', locals(), RequestContext(request))


def error404(request):
    info = 'Nie znaleziono strony'
    return render_to_response('notfound.html', locals(), RequestContext(request))

