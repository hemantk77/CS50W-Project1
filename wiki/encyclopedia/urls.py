from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.title_open, name="title_open"),
    path("search/", views.search_results, name='search_view'),
    path("new/", views.create_page, name='create_view'),
]
