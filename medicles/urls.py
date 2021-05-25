from django.urls import path
from . import views

app_name='medicles'

urlpatterns = [
    path('', views.index, name='index' ),
]

