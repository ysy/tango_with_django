from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.form import CategoryForm
from rango.form import PageForm


def index(request):
    # dict = {
    #     "blodmessage" : "Curnchy, creamy, cookies, candy, cpucake!"
    # }
    # return render(request, 'rango/index.html', context=dict)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {"categories": category_list, "pages": page_list}
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


def add_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid() and cat is not None:
            page = form.save(commit=False)
            page.views = 0
            page.category = cat
            page.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)
    return render(request, "rango/add_page.html", {'form': form, 'category': cat})


def about(request):
    dict = {"about_message": "this is about page"
        , "myname": "YuanSuyi"}
    return render(request, "rango/about.html", context=dict)
