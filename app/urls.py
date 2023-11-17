from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('all_professions', views.all_professions),
    path('comparison', views.comparison, name="comparison"),
    path('profession', views.profession),
    path('find_similar', views.find_similar, name="similar"),
]