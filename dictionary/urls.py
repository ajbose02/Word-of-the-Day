from django.urls import path
from . import views

app_name = 'dictionary'
urlpatterns = [
    path('', views.index, name='index'),
    path('words/', views.words, name='words'),
    path('words/<int:year>/<int:month>/<int:day>/', views.word, name="word"),
]
