from django.shortcuts import render, redirect, get_object_or_404
from main.models import Main
from news.models import News
from .models import Cat
import csv
from django.http import HttpResponse


def cat_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    cat = Cat.objects.all()
    return render(request, 'back/cat_list.html', {'cat': cat})


def cat_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if request.method == 'POST':
        name = request.POST.get('name')
        if name == "":
            error = "Something is wrong"
            return render(request, 'back/error.html', {'error': error})

        if len(Cat.objects.filter(name=name)) != 0:
            error = "Already created category"
            return render(request, 'back/error.html', {'error': error})

        b = Cat(name=name)
        b.save()
        return redirect('cat_list')
    return render(request, 'back/cat_add.html')


def export_cat_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment; filename="cat.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Counter'])

    for i in Cat.objects.all():
        writer.writerow([i.name, i.count])

    return response


def import_cat_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            error = "Please Input Csv File"
            return render(request, 'back/error.html', {'error': error})

        if csv_file.multiple_chunks():
            error = "File Too Large"
            return render(request, 'back/error.html', {'error': error})

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        for line in lines:
            fields = line.split(",")

            try:
                if len(Cat.objects.filter(name=fields[0])) == 0 and fields[0] != 'Title' and fields[0] != []:
                    b = Cat(name=fields)
                    b.save()

            except:
                print("Finish")

    return redirect('cat_list')
