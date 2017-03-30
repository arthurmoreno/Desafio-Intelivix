# coding=utf-8
import csv

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render, render_to_response

from utils import get_short_code
from models import Urls


# View that authenticate a user in the system
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            # TODO: fazer o erro de invalid login
            return render(request, 'registration/login.html')
    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'registration/login.html', context)


# View that logout a user
def logout_view(request):
    logout(request)
    return redirect('/login/')


# View that render the home page
@login_required
def home(request):
    urls = Urls.objects.filter(user=request.user)
    context = {
        'urls': urls
    }
    return render(request, 'home.html', context)


# View that redirects some shorten url to the original page
def redirect_original(short_id):
    url = get_object_or_404(Urls, pk=short_id)
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.http_url)


# View that shortens a url and saves it in the database
@login_required
def shorten_url(request):
    url = request.POST.get("url", '')
    if not (url == ''):
        short_id = get_short_code()
        url = Urls(user=request.user, http_url=url, short_id=short_id)
        url.save()

        urls = Urls.objects.filter(user=request.user)
        context = {
            'short_url': settings.SITE_URL + short_id,
            'urls': urls,
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html')


# View that search some url on the database
@login_required
def search_url(request):
    short_id = request.POST.get("short_id", '')
    urls = Urls.objects.filter(user=request.user)
    try:
        searched_url = Urls.objects.get(short_id=short_id)
    except ObjectDoesNotExist:
        searched_url = None
    context = {
        'searched_url': searched_url,
        'urls': urls
    }
    return render_to_response('search_result.html', context)


# View that return a cvs file containing the user urls
def export_cvs(request):
    urls = Urls.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['Short id', 'Original url', 'Data de publicação', 'Acessos'])
    for url in urls:
        writer.writerow([url.short_id, url.http_url, url.pub_date, url.count])
    return response
