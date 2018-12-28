from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lyrics/', views.lyrics, name='lyrics'),
    path('search_songs/', views.search_songs, name='search_songs'),
    path('all_songs/', views.all_songs, name='all_songs')
]
