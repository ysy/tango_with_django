from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page



def index(request):
    # dict = {
    #     "blodmessage" : "Curnchy, creamy, cookies, candy, cpucake!"
    # }
    # return render(request, 'rango/index.html', context=dict)
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {"categories": category_list}
    return render(request, 'rango/index.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=cat)

        context_dict["pages"] = pages
        context_dict["category"] = cat
    except Category.DoesNotExist:
        context_dict["pages"] = None
        context_dict["category"] = None

    return render(request, "rango/category.html", context_dict)

def about(request):
    dict = { "about_message": "this is about page"
             , "myname" : "YuanSuyi"}
    return render(request, "rango/about.html", context=dict)
