from django.urls import path
from . import views

app_name='medicles'

urlpatterns = [
    path('', views.index, name='index' ),
    path('search/', views.search, name='search'),
    path('tag/<int:article_id>/', views.add_tag, name='tag'),
    path('autocomplete/', views.ajax_load_tag, name='ajax_load_tag')
]

