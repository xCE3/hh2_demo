from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^new$', views.new),
    url(r'^(?P<id>\d+)/edit$', views.edit),
    url(r'^(?P<id>\d+)$', views.display),
    url(r'^users/(?P<id>\d+)$', views.job_user),
    url(r'^update$', views.update)
]