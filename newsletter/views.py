from django.shortcuts import render, redirect, get_object_or_404
from .models import Newsletter
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
from django.contrib.auth.models import User, Group, Permission
from manager.models import Manager
from main.models import Main
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.

def news_letter(request):
    if request.method == 'POST':
        txt = request.POST.get('txt')

        res = txt.find('@')
        if int(res) != -1:
            b = Newsletter(txt=txt, status=1)
            b.save()

        else:
            try:
                int(txt)
                b = Newsletter(txt=txt, status=2)
                b.save()
            except:
                return redirect('home')

    return redirect('home')


def news_emails(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    emails = Newsletter.objects.filter(status=1)

    return render(request, 'back/emails.html', {'emails': emails})


def news_phones(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    phones = Newsletter.objects.filter(status=2)

    return render(request, 'back/phones.html', {'phones': phones})


def news_txt_del(request, pk, num):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    b = Newsletter.objects.get(pk=pk)
    b.delete()
    if int(num) == 2:
        return redirect('news_phones')

    return redirect('news_emails')


def send_email(request):
    if request.method == 'POST':
        txt = request.POST.get('txt')
        subject = request.POST.get('name')

        a = []
        for i in Newsletter.objects.all():
            a.append(Newsletter.objects.get(pk=i.pk).txt)

        subjects = subject
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = a
        send_mail(subjects, message, email_from, emails)

    return redirect('news_emails')


def check_mychecklist(request):
    try:
        if request.method == 'POST':

            # for i in Newsletter.objects.filter(status=1):
            #     x = request.POST.get(str(i.pk))
            #     print(x)
            #     if str(x) == 'on':
            #         b= Newsletter.objects.get(pk=i.pk)
            #         b.delete()

            check = request.POST.getlist('checks[]')
            
            print(check)
            for i in check:
                b = Newsletter.objects.get(pk=i).txt
                b.delete()
    except:
        error = "You don't Delete"
        return render(request, 'back/error.html', {'error': error})

    return redirect('news_emails')
