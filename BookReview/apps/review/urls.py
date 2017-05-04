from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^books/add$', views.addbooks),
    url(r'^logout$', views.logout),
    url(r'^postbooks$', views.postbooks),
    url(r'^books/(?P<id>\d+)$', views.book, name = 'show_book'),
    url(r'^postreview/(?P<id>\d+)$', views.postreview),
    url(r'^users/(?P<id>\d+)$', views.viewuser),
]
