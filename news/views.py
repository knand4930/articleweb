from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending
import random
from comment.models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
import speech_recognition as sr
import pyttsx3
import wolframalpha
import wikipedia
import webbrowser
from django.contrib import messages


# Create your views here.
mysearch = ""


def news_details(request, word):
    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    shownews = News.objects.filter(name=word)[:3]
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    tagname = News.objects.get(name=word).tag
    tag = tagname.split(',')
    trending = Trending.objects.all().order_by('-pk')[:5]

    try:
        mynews = News.objects.get(name=word)
        mynews.show = mynews.show + 1
        mynews.save()

    except:
        print("something went wrong")

    code = News.objects.get(name=word).pk
    comment = Comment.objects.filter(news_id=code, status=1).order_by('-pk')[:10]
    cmcount = len(comment)

    link = "/urls/" + str(News.objects.get(name=word).rand)

    return render(request, 'front/news_details.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'shownews': shownews,
                   'popnews': popnews, 'popnews2': popnews2, 'tag': tag, 'tagname': tagname, 'trending': trending,
                   'code': code, 'comment': comment, 'cmcount': cmcount, 'link': link})


def news_details_short(request, pk):
    site = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    shownews = News.objects.filter(rand=pk)[:3]
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    tagname = News.objects.get(rand=pk).tag
    tag = tagname.split(',')
    trending = Trending.objects.all().order_by('-pk')[:5]

    try:
        mynews = News.objects.get(rand=pk)
        mynews.show = mynews.show + 1
        mynews.save()

    except:
        messages.warning(request, 'Some thing went wrong')

    return render(request, 'front/news_details.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'shownews': shownews,
                   'popnews': popnews, 'popnews2': popnews2, 'tag': tag, 'tagname': tagname, 'trending': trending})


def news_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': prem = 1

    if prem == 0:
        news = News.objects.filter(writer=request.user)
    elif prem == 1:
        newss = News.objects.all()
        paginator = Paginator(newss, 10)
        page = request.GET.get('page')

        try:
            news = paginator.page(page)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            news = paginator.page(1)

    return render(request, 'back/article_list.html', {'news': news})


def news_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

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

    date = str(year) + str(month) + str(day)
    randint = str(random.randint(1000, 9999))
    rand = date + randint
    rand = int(rand)

    while len(News.objects.filter(rand=rand)) != 0:
        randint = str(random.randint(1000, 9999))
        rand = date + randint
        rand = int(rand)

    cat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        if newstitle == "" or newscat == " " or newstxtshort == "" or newstxt == "" or newscat == "":
            error = "All Field is Required"
            return render(request, 'back/error.html', {'error': error})

        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    newsname = SubCat.objects.get(pk=newsid).name
                    ocatid = SubCat.objects.get(pk=newsid).catid

                    b = News(name=newstitle, short_txt=newstxtshort, body_txt=newstxt, date=today, time=time,
                             picname=filename,
                             picurl=url, writer=request.user,
                             catname=newsname, catid=newsid, ocatid=ocatid, show=0, tag=tag, rand=rand)
                    b.save()

                    count = len(News.objects.filter(ocatid=ocatid))

                    b = Cat.objects.get(pk=ocatid)
                    b.count = count
                    b.save()
                    return redirect('news_list')

                else:
                    error = "Your File Longer Than 5MP"
                    return render(request, 'back/error.html', {'error': error})

            else:
                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your File Not Supported"
                return render(request, 'back/error.html', {'error': error})




        except:
            error = "Please Input in your image"
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'back/add_article.html', {'cat': cat})


def news_delete(request, pk):
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

    try:
        b = News.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(b.picname)

        ocatid = News.objects.get(pk=pk).ocatid

        b.delete()

        count = len(News.objects.filter(ocatid=ocatid))

        m = Cat.objects.get(pk=ocatid)
        m.count = count
        m.save()


    except:
        error = "Something Wrong"
        return render(request, 'back/error.html', {'error': error})

    return redirect('news_list')


def article_edit(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if len(News.objects.filter(pk=pk)) == 0:
        error = "News Not Found"
        return render(request, 'back/error.html', {'error': error})

    prem = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': prem = 1

    if prem == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied"
            return render(request, 'back/error.html', {'error': error})

    news = News.objects.get(pk=pk)
    cat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        if newstitle == "" or newscat == " " or newstxtshort == "" or newstxt == "" or newscat == "":
            error = "All Field is Required"
            return render(request, 'back/error.html', {'error': error})

        try:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000:

                    newsname = SubCat.objects.get(pk=newsid).name

                    b = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.picname)

                    b.name = newstitle
                    b.short_txt = newstxtshort
                    b.body_txt = newstxt
                    b.picname = filename
                    b.picurl = url
                    b.catname = newsname
                    b.catid = newsid
                    b.tag = tag
                    b.act = 0
                    b.save()
                    return redirect('news_list')

                else:
                    error = "Your File Longer Than 5MP"
                    return render(request, 'back/error.html', {'error': error})

            else:
                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your File Not Supported"
                return render(request, 'back/error.html', {'error': error})




        except:
            newsname = SubCat.objects.get(pk=newsid).name

            b = News.objects.get(pk=pk)

            b.name = newstitle
            b.short_txt = newstxtshort
            b.body_txt = newstxt
            b.catname = newsname
            b.catid = newsid
            b.tag = tag
            b.save()
            return redirect('news_list')

    return render(request, 'back/article_edit.html', {'pk': pk, 'news': news, 'cat': cat})


def news_publish(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    news = News.objects.get(pk=pk)
    news.act = 1
    news.save()

    return redirect('news_list')


def news_all_show(request, word):
    catid = Cat.objects.get(name=word).pk
    allnewss = News.objects.filter(ocatid=catid)

    site = Main.objects.get(pk=1)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    paginator = Paginator(allnewss, 12)
    page = request.GET.get('page')
    try:
        allnews = paginator.page(page)
    except EmptyPage:
        allnews = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        allnews = paginator.page(1)

    return render(request, 'front/all_news.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews,
                   'popnews2': popnews2, 'trending': trending, 'lastnews2': lastnews2, 'allnewss': allnewss})


def all_news(request):
    allnewss = News.objects.all()

    site = Main.objects.get(pk=1)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1:
        day = "0" + str(day)

    if len(str(month)) == 1:
        month = "0" + str(month)

    today = str(year) + "/" + str(month) + "/" + str(day)

    f_rom = []
    t_o = []

    for i in range(28):
        b = datetime.datetime.now() - datetime.timedelta(days=i)
        year = b.year
        month = b.month
        day = b.day

        if len(str(day)) == 1:
            day = "0" + str(day)

        if len(str(month)) == 1:
            month = "0" + str(month)
        b = str(year) + "/" + str(month) + "/" + str(day)

        f_rom.append(b)

        c = datetime.datetime.now() - datetime.timedelta(days=i)
        year = c.year
        month = c.month
        day = c.day

        if len(str(day)) == 1:
            day = "0" + str(day)

        if len(str(month)) == 1:
            month = "0" + str(month)
        c = str(year) + "/" + str(month) + "/" + str(day)
        t_o.append(c)

    paginator = Paginator(allnewss, 12)
    page = request.GET.get('page')
    try:
        allnews = paginator.page(page)
    except EmptyPage:
        allnews = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        allnews = paginator.page(1)

    return render(request, 'front/all_news_2.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews,
                   'popnews2': popnews2, 'trending': trending, 'lastnews2': lastnews2, 'allnewss': allnewss,
                   'f_rom': f_rom, 't_o': t_o})


def all_news_search(request):
    try:
        if request.method == 'POST':
            txt = request.POST.get('txt')
            catid = request.POST.get('cat')
            f_rom = request.POST.get('from')
            t_o = request.POST.get('to')
            mysearch = txt

            if f_rom != "0" and t_o != "0":
                if t_o < f_rom:
                    msg = "Your Date is very littale than form date"
                    return render(request, 'back/msgbox.html', {'msg': msg})

            if catid == "0":

                if f_rom != "0" and t_o != "0":
                    a = News.objects.filter(name__contains=txt, date__gte=f_rom, date__lte=t_o)
                    b = News.objects.filter(short_txt__contains=txt, date__gte=f_rom, date__lte=t_o)
                    c = News.objects.filter(body_txt__contains=txt, date__gte=f_rom, date__lte=t_o)

                elif f_rom != "0":
                    a = News.objects.filter(name__contains=txt, date__gte=f_rom)
                    b = News.objects.filter(short_txt__contains=txt, date__gte=f_rom)
                    c = News.objects.filter(body_txt__contains=txt, date__gte=f_rom)

                elif t_o != "0":
                    a = News.objects.filter(name__contains=txt, date__lte=t_o)
                    b = News.objects.filter(short_txt__contains=txt, date__lte=t_o)
                    c = News.objects.filter(body_txt__contains=txt, date__lte=t_o)




                else:
                    a = News.objects.filter(name__contains=txt)
                    b = News.objects.filter(short_txt__contains=txt)
                    c = News.objects.filter(body_txt__contains=txt)



            else:

                if f_rom != "0" and t_o != "0":
                    a = News.objects.filter(name__contains=txt, ocatid=catid, date__gte=f_rom, date__lte=t_o)
                    b = News.objects.filter(short_txt__contains=txt, ocatid=catid, date__gte=f_rom, date__lte=t_o)
                    c = News.objects.filter(body_txt__contains=txt, ocatid=catid, date__gte=f_rom, date__lte=t_o)


                elif f_rom != "0":
                    a = News.objects.filter(name__contains=txt, ocatid=catid, date__gte=f_rom)
                    b = News.objects.filter(short_txt__contains=txt, ocatid=catid, date__gte=f_rom)
                    c = News.objects.filter(body_txt__contains=txt, ocatid=catid, date__gte=f_rom)

                if t_o != "0":
                    a = News.objects.filter(name__contains=txt, ocatid=catid, date__lte=t_o)
                    b = News.objects.filter(short_txt__contains=txt, ocatid=catid, date__lte=t_o)
                    c = News.objects.filter(body_txt__contains=txt, ocatid=catid, date__lte=t_o)



                else:
                    a = News.objects.filter(name__contains=txt, ocatid=catid)
                    b = News.objects.filter(short_txt__contains=txt, ocatid=catid)
                    c = News.objects.filter(body_txt__contains=txt, ocatid=catid)

            allnewss = list(chain(a, b, c))
            allnewss = list(dict.fromkeys((allnewss)))


        else:

            if catid == "0":

                if f_rom != "0" and t_o != "0":
                    a = News.objects.filter(name__contains=mysearch, date__gte=f_rom, date__lte=t_o)
                    b = News.objects.filter(short_txt__contains=mysearch, date__gte=f_rom, date__lte=t_o)
                    c = News.objects.filter(body_txt__contains=mysearch, date__gte=f_rom, date__lte=t_o)


                elif f_rom != "0":
                    a = News.objects.filter(name__contains=mysearch, date__gte=f_rom)
                    b = News.objects.filter(short_txt__contains=mysearch, date__gte=f_rom)
                    c = News.objects.filter(body_txt__contains=mysearch, date__gte=f_rom)

                if t_o != "0":
                    a = News.objects.filter(name__contains=mysearch, date__lte=t_o)
                    b = News.objects.filter(short_txt__contains=mysearch, date__lte=t_o)
                    c = News.objects.filter(body_txt__contains=mysearch, date__lte=t_o)




                else:
                    a = News.objects.filter(name__contains=mysearch)
                    b = News.objects.filter(short_txt__contains=mysearch)
                    c = News.objects.filter(body_txt__contains=mysearch)




            else:

                if f_rom != "0" and t_o != "0":
                    a = News.objects.filter(name__contains=mysearch, ocatid=catid, date__gte=f_rom, date__lte=t_o)
                    b = News.objects.filter(short_txt__contains=mysearch, ocatid=catid, date__gte=f_rom, date__lte=t_o)
                    c = News.objects.filter(body_txt__contains=mysearch, ocatid=catid, date__gte=f_rom, date__lte=t_o)

                if f_rom != "0":
                    a = News.objects.filter(name__contains=mysearch, ocatid=catid, date__gte=f_rom)
                    b = News.objects.filter(short_txt__contains=mysearch, ocatid=catid, date__gte=f_rom)
                    c = News.objects.filter(body_txt__contains=mysearch, ocatid=catid, date__gte=f_rom)

                if t_o != "0":
                    a = News.objects.filter(name__contains=mysearch, ocatid=catid, date__lte=t_o)
                    b = News.objects.filter(short_txt__contains=mysearch, ocatid=catid, date__lte=t_o)
                    c = News.objects.filter(body_txt__contains=mysearch, ocatid=catid, date__lte=t_o)


                else:
                    a = News.objects.filter(name__contains=mysearch, ocatid=catid)
                    b = News.objects.filter(short_txt__contains=mysearch, ocatid=catid)
                    c = News.objects.filter(body_txt__contains=mysearch, ocatid=catid)

            allnewss = list(chain(a, b, c))
            allnewss = list(dict.fromkeys((allnewss)))

        site = Main.objects.get(pk=1)
        news = News.objects.filter(act=1).order_by('-pk')
        cat = Cat.objects.all()
        subcat = SubCat.objects.all()
        lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
        popnews = News.objects.filter(act=1).order_by('-show')
        popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
        trending = Trending.objects.all().order_by('-pk')[:5]
        lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        if len(str(day)) == 1:
            day = "0" + str(day)

        if len(str(month)) == 1:
            month = "0" + str(month)

        today = str(year) + "/" + str(month) + "/" + str(day)

        f_rom = []
        t_o = []

        for i in range(28):
            b = datetime.datetime.now() - datetime.timedelta(days=i)
            year = b.year
            month = b.month
            day = b.day

            if len(str(day)) == 1:
                day = "0" + str(day)

            if len(str(month)) == 1:
                month = "0" + str(month)
            b = str(year) + "/" + str(month) + "/" + str(day)

            f_rom.append(b)

            c = datetime.datetime.now() - datetime.timedelta(days=i)
            year = c.year
            month = c.month
            day = c.day

            if len(str(day)) == 1:
                day = "0" + str(day)

            if len(str(month)) == 1:
                month = "0" + str(month)
            c = str(year) + "/" + str(month) + "/" + str(day)
            t_o.append(c)

        paginator = Paginator(allnewss, 12)
        page = request.GET.get('page')

        try:
            allnews = paginator.page(page)

        except EmptyPage:
            allnews = paginator.page(paginator.num_pages)

        except PageNotAnInteger:
            allnews = paginator.page(1)
    except:
        msg = "You don't Search This field"
        return render(request, 'front/msgbox.html', {'msg': msg})

    return render(request, 'front/all_news_2.html',
                  {'site': site, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews,
                   'popnews2': popnews2, 'trending': trending, 'lastnews2': lastnews2, 'allnewss': allnewss,
                   'f_rom': f_rom, 't_o': t_o})


def bot_search(request):
    query = request.GET.get('query')

    try:
        client = wolframalpha.Client("KA2W5A-VV99TYYW8K")
        res = client.query(query)
        ans = next(res.results).text
        return render(request, 'back/bot_search.html', {'ans': ans, 'query': query})


    except Exception:
        try:
            ans = wikipedia.summary(query, sentences=39000)
            return render(request, 'back/bot_search.html', {'ans': ans, 'query': query})


        except Exception:
            ans = "Please Your Search Query"
            return render(request, 'back/bot_search.html', {'ans': ans, 'query': query})

# News.objects.filter(pk=pk).exclude(date__gte="2020/01/01")
