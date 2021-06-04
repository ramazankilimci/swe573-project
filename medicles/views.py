from typing import ContextManager
from django.http import response
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from medicles.models import Article
import json

# Create your views here.

def index(request):
    context = "Welcome to medicles!"
    return render(request, 'medicles/index.html')

def search(request):
    search_term = request.GET.get('q', None)
    if not search_term:
        raise Http404('Please enter a word at least!')
    
    articles = Article.objects.search(search_term)

    response_data = [
        {
            'rank': article.rank,
            'title': article.title,
            'url': article.get_absolute_url(),
        } for article in articles
    ]

    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )