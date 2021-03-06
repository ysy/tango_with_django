from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import  reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from rango.models import Category
from rango.models import Page
from rango.form import CategoryForm
from rango.form import PageForm
from rango.form import UserForm
from rango.form import UserProfileForm


def get_server_side_cookie(request, cookie, default=""):
    val = request.session.get(cookie)
    if not val:
        val = default
    return val


def visitor_cookie_handler(request):
    visits = get_server_side_cookie(request, 'visits', 1)
    last_visit_time = get_server_side_cookie(request, 'last_visit', datetime.now().timestamp())

    try:
        if (datetime.now() - datetime.fromtimestamp(last_visit_time)).seconds > 3:
            visits += 1
            last_visit_time = datetime.now().timestamp()
    except ValueError:
        visits = 1
        last_visit_time = datetime.now().timestamp()

    request.session['visits'] = visits
    request.session['last_visit'] = last_visit_time


def index(request):
    # dict = {
    #     "blodmessage" : "Curnchy, creamy, cookies, candy, cpucake!"
    # }
    # return render(request, 'rango/index.html', context=dict)
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {"categories": category_list, "pages": page_list}
    response = render(request, 'rango/index.html', context_dict)
    visitor_cookie_handler(request)
    return response


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


@login_required
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


@login_required
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
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED")
        request.session.delete_test_cookie()
    context_dict = {"about_message": "this is about page",
                    "myname": "YuanSuyi"}
    visitor_cookie_handler(request)
    return render(request, "rango/about.html", context=context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.erros)
            print(profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('You are not loged')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return  HttpResponse('Your account is locked')
        else:
            return HttpResponse('Invalid login details supplied')
    else:
        return render(request, 'rango/login.html', {})


@login_required()
def restricted(request):
    return render(request, "rango/restricted.html", {})


def track_url(request):
    page_id = request.GET.get('page_id', None)
    url = reverse('index')
    try:
        if page_id is not None:
            page_id = int(page_id)
            page = Page.objects.get(id=page_id)
            if page is not None:
                url = page.url
                page.views += 1
                page.save()
    except ValueError:
        pass
    return HttpResponseRedirect(url)
