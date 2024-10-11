#home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),  # Home page view
    path('runcode', views.runcode, name="runcode"), # Code execution view
    path('recent_codes/', views.recent_codes, name='recent_codes'),
]
