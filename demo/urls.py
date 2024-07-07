
from django.urls import path
from . import views

urlpatterns = [
path("hello/", views.say_hello),
path("hello1/<str:name>/", views.welcome),
path("html/", views.say_hello2)
]