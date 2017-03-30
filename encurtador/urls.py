from django.conf.urls import url
from django.contrib import admin
from django.views.generic import CreateView
from django.core.urlresolvers import reverse

from urlsApp import views as urlsapp_view
from urlsApp.forms import UserCreationCustomForm


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Authenticate system
    url(r'^login/$', urlsapp_view.login_view, name='login_view'),
    url(r'^logout/$', urlsapp_view.logout_view, name='logout_view'),
    url(r'^create_user/$', (CreateView.as_view(get_success_url=lambda: reverse('login_view'),
                                               form_class=UserCreationCustomForm,
                                               template_name="create_user.html")), name='create_user'),

    # Url App
    url(r'^$', urlsapp_view.home, name='home'),
    url(r'^shorten/$', urlsapp_view.shorten_url, name='shorten'),
    url(r'^export_cvs/$', urlsapp_view.export_cvs, name='export_cvs'),
    url(r'^search/$', urlsapp_view.search_url, name='search_url'),
    url(r'^(?P<short_id>\w{6})$', urlsapp_view.redirect_original, name='redirect_original'),
]





