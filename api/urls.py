from django.urls import path, reverse
from django.shortcuts import redirect
from .views import *

urlpatterns = [
    path('check/', DayDateView.as_view()),
    path('delete/', DeleteDate.as_view()),



]
