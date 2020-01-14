from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    dict = {
        "blodmessage" : "Curnchy, creamy, cookies, candy, cpucake!"
    }
    return render(request, 'rango/index.html', context=dict)

def about(request):
    dict = { "about_message": "this is about page"
             , "myname" : "YuanSuyi"}
    return render(request, "rango/about.html", context=dict)
