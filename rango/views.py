from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    dict = {
        "blodmessage" : "Curnchy, creamy, cookies, candy, cpucake!"
    }
    return render(request, 'rango/index.html', context=dict)

def about(request):
    return HttpResponse("""
    
    <h1> Rango says here is about page </h1>
     <a href=/rango><h1>Main Page</h1></a>
    """)