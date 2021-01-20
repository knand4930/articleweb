from django.shortcuts import render, redirect, get_object_or_404
from .models import BlackList
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


# Create your views here.

def black_list(request):
    ip = BlackList.objects.all()

    return render(request, 'back/blacklist.html', {'ip': ip})


def ip_add(request):
    if request.method == 'POST':
        ip = request.POST.get('ip')
        if ip != "":
            b = BlackList(ip=ip)
            b.save()

    return redirect('black_list')


def ip_del(request, pk):
    b = BlackList.objects.filter(pk=pk)
    b.delete()

    return redirect('black_list')
