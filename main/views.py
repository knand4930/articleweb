from django.shortcuts import render, redirect, get_object_or_404
from .models import Main
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
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from blacklist.models import BlackList
from django.core.mail import send_mail
from django.conf import settings
from contactform.models import ContactForm
from zeep import Client
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import urllib.request as urllib2
from rest_framework import viewsets
from .serializer import NewsSerializer
from newsletter.models import Newsletter
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from email.message import EmailMessage
import smtplib
from django.conf import settings



# Create your views here.
@csrf_exempt
def home(request):
    site = Main.objects.get(pk=1)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    # soup
    # client = Client('hackingpart.wsdl')
    # result = client.service.funcname(1,2,3,4,5,6,7)
    # print(result)

    # Curl
    # url = 'https://www.google.com'
    # payload = {'a':"b", 'c':"d"}
    # result = requests.post(url, params= payload)
    # print(result.url)
    # print(result)
    # result.status_code

    # json
    # url = 'https://www.google.com/'
    # data = {'a': "b", 'c': "d"}
    # headers = {'Content_Type': 'application/json', 'API_KEY': 'google.com'}
    # result = request.post(url, data=json.dumps(data), headers=headers)
    # print(result)

    # return redirect('https://google.com')

    # my_html= """
    #
    # <title>This is a Test </title>
    #
    #     """
    # soup = BeautifulSoup(my_html,'html.parser')
    # print(soup.title)
    # print(soup.title.string)

    # url = "https://google.com"
    # result =requests.post(url)
    # print(result.content)

    # url = 'https://google.com'
    # opener = urllib2.build_opener()
    # content = opener.open(url).read()
    # soup = BeautifulSoup(content)
    # print(soup.title.string)

    # url = 'http://127.0.0.1:8000/show/data/'
    # opener = urllib2.build_opener()
    # content = opener.open(url).read()
    # print(content)

    request.session['test'] = 'hello'
    print(request.session['test'])

    return render(request, 'front/home.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews,
                   'popnews2': popnews2, 'trending': trending, 'lastnews2': lastnews2})


def about(request):
    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')

    return render(request, 'front/about.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews,
                   'popnews2': popnews2, 'trending': trending})


def panel(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.codename == 'master_user': perm = 1

    '''
    test = ['!', '@', '#', '$', '%', '^', '&', '*']
    rand = ""
    for i in range(5):
        rand = rand + random.choice(string.ascii_letters)
        rand += random.choice(test)
        rand += str(random.randint(0,9))
    
    count = News.objects.count()
    rand = News.objects.all()[randint(0, count-1)]
    '''

    return render(request, 'back/panel.html', {})


def mylogin(request):
    if request.method == 'POST':
        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "":
            user = authenticate(username=utxt, password=ptxt)

            if user != None:
                login(request, user)
                return redirect('panel')

    return render(request, 'front/login.html')


def myregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == "":
            msg = "Input your Full Name"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if password1 != password2:
            msg = "Your Password Didn't Match"
            return render(request, 'front/msgbox.html', {'msg': msg})

        count1 = 0
        count2 = 0
        count3 = 0
        for i in password1:

            if "0" < i < "9":
                count1 = 1
            if "A" < i < "Z":
                count2 = 1
            if "a" < i < "z":
                count3 = 1

        if count1 == 0 or count2 == 0 or count3 == 0:
            msg = "Your Password Not Stronger"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if len(password1) < 8:
            msg = "your password must be 8 character"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0:

            ip, is_routable = get_client_ip(request)

            if ip is None:
                ip = "0.0.0.0"

            try:
                response = DbIpCity.get(ip, api_key='free')
                country = response.country + "|" + response.city
            except:
                country = "Unknown"

            user = User.objects.create_user(username=uname, email=email, password=password1)
            b = Manager(name=name, utxt=uname, email=email, ip=ip, country=country)
            b.save()

    return render(request, 'front/login.html')


def mylogout(request):
    logout(request)

    return redirect('mylogin')


def site_setting(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': prem = 1

    if prem == 0:
        error = "Access Denied "
        return render(request, 'back/error.html', {'error': error})

    if request.method == 'POST':
        name = request.POST.get('name')
        tell = request.POST.get('tell')
        pinterest = request.POST.get('pinterest')
        twitter = request.POST.get('twitter')
        youtube = request.POST.get('youtube')
        facebook = request.POST.get('facebook')
        linkedin = request.POST.get('linkedin')
        link = request.POST.get('link')
        txt = request.POST.get('txt')
        seo_txt = request.POST.get('seotxt')
        seo_keyword = request.POST.get('seokeyword')

        if facebook == " ": facebook = "#"
        if twitter == " ": twitter = "#"
        if pinterest == " ": pinterest = "#"
        if youtube == " ": youtube = "#"
        if linkedin == " ": linkedin = "#"
        if link == " ": link = "#"

        if name == " " or tell == "" or txt == "":
            error = "Name Phone no. and Abouts us is required"
            return render(request, 'back/error.html', {'error': error})

        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            picurl = url
            picname = filename

        except:

            picurl = "-"
            picname = "-"

        try:

            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url = fs2.url(filename2)

            picurl2 = url2
            picname2 = filename2

        except:

            picurl2 = "-"
            picname2 = "-"

        b = Main.objects.get(pk=1)
        b.name = name
        b.tell = tell
        b.facebook = facebook
        b.linkedin = linkedin
        b.link = link
        b.about = txt
        b.twitter = twitter
        b.pinterest = pinterest
        b.youtube = youtube
        b.seo_txt = seo_txt
        b.seo_keyword = seo_keyword

        if picurl != "-": b.picname = picurl
        if picname != "-": b.picname = picname

        if picurl2 != "-": b.picname = picurl2
        if picname2 != "": b.picname = picname2

        b.save()

    site = Main.objects.get(pk=1)

    return render(request, 'back/setting.html', {'site': site})


def about_setting(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': prem = 1

    if prem == 0:
        error = "Access Denied "
        return render(request, 'back/error.html', {'error': error})

    if request.method == 'POST':
        txt = request.POST.get('txt')

        if txt == "":
            error = "All Field is Required"
            return render(request, 'back/error.html', {'error': error})

        b = Main.objects.get(pk=1)
        b.abouttxt = txt
        b.save()

    about = Main.objects.get(pk=1).abouttxt

    return render(request, 'back/about_setting.html', {'about': about})


def contact(request):
    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    return render(request, 'front/contact.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews,
                   'popnews2': popnews2, 'trending': trending})


def change_pass(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if request.method == 'POST':
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "":
            error = "All Field is Required"
            return render(request, 'back/error.html', {'error': error})

        user = authenticate(username=request.user, password=oldpass)

        if user != None:
            if len(newpass) < 8:
                error = "Your Password at least minimum 8 character"
                return render(request, 'back/error.html', {'error': error})

            count1 = 0
            count2 = 0
            count3 = 0
            for i in newpass:

                if "0" < i < "9":
                    count1 = 1
                if "A" < i < "Z":
                    count2 = 1
                if "a" < i < "z":
                    count3 = 1

            if count1 == 1 and count2 == 1 and count3 == 1:
                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect('mylogout')




        else:

            error = "Your Password Not Correct"
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'back/changepass.html', {})


def change_admin(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    try:
        if request.method == 'POST':
            oldadmin = request.POST.get('oldadmin')
            newadmin = request.POST.get('newadmin')
            try:
                user = User.objects.get(username=oldadmin)
                user.username = newadmin
                user.save()
                return redirect('mylogout')
            except:
                error = "Please Input Correct Username"
                return render(request, 'back/error.html', {'error': error})

    except:
        error = "This User Name is Already"
        return render(request, 'back/error.html', {'error': error})

    return render(request, 'back/changeadmin.html', {})


def answer_cm(request, pk):
    if request.method == 'POST':
        txt = request.POST.get('txt')
        subject = request.POST.get('name')

        if txt == "":
            error = "Please Type Your Answer"
            return render(request, 'back/error.html', {'error': error})

        to_email = ContactForm.objects.get(pk=pk).email
        subjects = subject
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = [to_email]
        send_mail(subjects, message, email_from, emails)

    return render(request, 'back/answer_cm.html', {'pk': pk})


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


def show_data(request):
    count = Newsletter.objects.filter(status=1).count()

    data = {'count': count}
    return JsonResponse(data)


def latest_article(request):
    site = Main.objects.get(pk=1)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')
    trending = Trending.objects.all().order_by('-pk')
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:50]

    return render(request, 'back/latest_article.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews,
                   'popnews2': popnews2, 'trending': trending, 'lastnews2': lastnews2})


def popular_article(request):
    site = Main.objects.get(pk=1)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')
    popnews = News.objects.filter(act=1).order_by('-show')[:50]
    popnews2 = News.objects.filter(act=1).order_by('-show')
    trending = Trending.objects.all().order_by('-pk')
    lastnews2 = News.objects.filter(act=1).order_by('-pk')

    return render(request, 'back/popular_article.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews,
                   'popnews2': popnews2, 'trending': trending, 'lastnews2': lastnews2, })


def users_profiles(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': prem = 1

    if prem == 0:
        error = "Access Denied "
        return render(request, 'back/error.html', {'error': error})

    if request.method == 'POST':
        name = request.POST.get('name')


        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            picurl = url
            picname = filename

        except:

            picurl = "-"
            picname = "-"

        try:

            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url = fs2.url(filename2)

            picurl2 = url2
            picname2 = filename2

        except:

            picurl2 = "-"
            picname2 = "-"

        try:

            myfile3 = request.FILES['myfile3']
            fs3 = FileSystemStorage()
            filename3 = fs3.save(myfile3.name, myfile3)
            url = fs3.url(filename3)

            picurl3 = url3
            picname3 = filename3

        except:

            picurl3 = "-"
            picname3 = "-"

        b = Main.objects.get(pk=1)

        if picurl != "-":
            b.picname = picurl
        if picname != "-":
            b.picname = picname

        if picurl2 != "-":
            b.picname = picurl2
        if picname2 != "":
            b.picname = picname2

        if picurl3 != "-":
            b.picname = picurl3
        if picname3 != "":
            b.picname = picname3

        b.save()

    site = Main.objects.get(pk=1)

    return render(request, 'back/user_profile.html',{'site':site})


