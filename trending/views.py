from django.shortcuts import render, redirect, get_object_or_404
from .models import Trending
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage


# Create your views here.

def tranding_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if request.method == 'POST':
        txt = request.POST.get('txt')

        if txt == "":
            error = "All Field is Required"
            return render(request, 'back/error.html', {'error': error})
        b = Trending(txt=txt)
        b.save()
    trendinglist = Trending.objects.all()

    return render(request, 'back/trending.html', {'trendinglist': trendinglist})


def trending_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    try:
        b = Trending.objects.filter(pk=pk)
        b.delete()
    except:
        error = "Something Wrong"
        return render(request, 'back/error.html', {'error': error})

    return redirect('tranding_add')


def trending_edit(request, pk):
    mytxt = Trending.objects.get(pk=pk).txt

    if request.method == 'POST':
        txt = request.POST.get('txt')
        if txt == "":
            error = "Something Wrong"
            return render(request, 'back/error.html', {'error': error})

        b = Trending.objects.get(pk=pk)
        b.txt = txt
        b.save()

        return redirect('tranding_add')
    return render(request, 'back/trending_edit.html', {'mytxt': mytxt, 'pk':pk})
