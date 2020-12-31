from django.urls import path

from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('auth', views.auth, name='auth'),
    path('logout', views.log_out, name='log_out'),
    path('registration', views.registration, name='registration'),
    path('activate/<uidb64>)/<token>', views.activate, name='activate'),
    path('profile', views.profile, name='profile'),
]
