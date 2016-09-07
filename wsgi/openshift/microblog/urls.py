__author__ = 'Joanna667'
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^edit/(?P<idd>\d+)$', views.edit, name="edit"),
    url(r'^users/(?P<idd>\d+)$', views.user_posts, name="userArticles"),
    url(r'^tagged/(?P<idd>\d+)$', views.tagged, name="tagged"),
    url(r'^users/register$', views.register, name="register"),
    url(r'^users/activate/(?P<key>.+)$', views.activate, name="activate"),
    url(r'^login$', views.log_in, name="login"),
    url(r'^logout$', views.log_out, name="logout"),
    url(r'^create$', views.create, name="create"),
    url(r'^', views.notfound,name='notfound')
)