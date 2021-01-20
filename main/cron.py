from blacklist.models import BlackList


def my_job():
    b = BlackList(ip="192.168.0.1")
    b.save()
