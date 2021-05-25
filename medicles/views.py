from typing import ContextManager
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    context = "Welcome to medicles!"
    return render(request, 'medicles/index.html')

