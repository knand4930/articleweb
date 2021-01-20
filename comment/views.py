from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
from django.contrib.auth.models import User, Group, Permission
from manager.models import Manager
import random
import string
from random import randint
import datetime
from django.contrib import messages


# Create your views here.

def news_cm_add(request, pk):
    try:
        if request.method == 'POST':
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            day = now.day
            hour = now.hour
            minutes = now.minute
            second = now.second

            if len(str(day)) == 1:
                day = "0" + str(day)

            if len(str(month)) == 1:
                month = "0" + str(month)

            today = str(year) + "/" + str(month) + "/" + str(day)
            time = str(hour) + ":" + str(minutes) + ":" + str(second)

            cm = request.POST.get('msg')

            if request.user.is_authenticated:

                manager = Manager.objects.get(utxt=request.user)

                b = Comment(name=manager.name, email=manager.email, news_id=pk, date=today, time=time, cm=cm)
                b.save()

            else:

                name = request.POST.get('name')
                email = request.POST.get('email')
                msg = request.POST.get('msg')
                b = Comment(name=name, email=email, cm=msg, news_id=pk, date=today, time=time)
                b.save()
    except:
        messages.success(request, "Admin Cann't Send Messages")

    newsname = News.objects.get(pk=pk).name
    return redirect('news_details', word=newsname)


def comments_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': prem = 1

    if prem == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied"
            return render(request, 'back/error.html', {'error': error})

    comment = Comment.objects.all()

    return render(request, 'back/comments_list.html', {'comment': comment})


def comments_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': prem = 1

    if prem == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied"
            return render(request, 'back/error.html', {'error': error})

    comment = Comment.objects.filter(pk=pk)
    comment.delete()

    return redirect('comments_list')


def comments_confirm(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': prem = 1

    if prem == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied"
            return render(request, 'back/error.html', {'error': error})

    comment = Comment.objects.get(pk=pk)
    comment.status = 1
    comment.save()

    return redirect('comments_list')
