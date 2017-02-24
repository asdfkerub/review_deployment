from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^fuckitall$',views.fuckit),
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^users/(?P<id>\d+)$',views.account),
    url(r'^books/add$',views.add),
    url(r'^books/add/process$',views.add_process),
    url(r'^books/(?P<book_id>\d+)$',views.book),
    url(r'^book/add_review/(?P<book_id>\d+)$',views.add_review),
    url(r'^books$',views.all_books),
    url(r'^delete/review/(?P<review_id>\d+)$',views.delete_review)

]
