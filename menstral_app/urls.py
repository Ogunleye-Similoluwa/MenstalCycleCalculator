from django.urls import path
from .views import CycleCreateView,MyLoginView,RegisterPage
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('cycle/create/', CycleCreateView.as_view(), name='create'),
    path('cycle/login/', MyLoginView.as_view(), name='login'),
    path('cycle/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('cycle/register/', RegisterPage.as_view(), name='register'),
]
