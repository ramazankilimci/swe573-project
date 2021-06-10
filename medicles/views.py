from medicles.forms import TagForm
from typing import ContextManager
from django.core import paginator
from django.http import response
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from medicles.models import Article, Tag
from medicles.services import Wikidata
from .forms import TagForm
# Create your views here.

def index(request):
    #context = "Welcome to medicles!"
    return render(request, 'medicles/index.html')

def search(request):
    search_term = request.GET.get('q', None)
    #search_term = 'covid'
    if not search_term:
        raise Http404('Please enter a word at least!')
    
    articles = Article.objects.search(search_term)
    context = {'articles': articles}
    #print(context)


    return render(request, 'medicles/search_results.html', {'articles': articles}) # add context variable if you want to go back

''' Working tag form. Simple, just adds one field to Article model.
def add_tag(request, article_id):
    if request.method =='POST':
        form = TagForm(request.POST)
        if form.is_valid():
            article_will_be_updated = Article.objects.get(pk=article_id)
            article_will_be_updated.tags = form.cleaned_data['tag_key'] + ":" + form.cleaned_data['tag_value']
            article_will_be_updated.save()
            print(form.cleaned_data['tag_key'], form.cleaned_data['tag_value'])
            return HttpResponseRedirect('/thanks')

    else:
        form = TagForm()

    return render(request, 'medicles/tag_create.html', {'form': form, 'article_id': article_id})
'''

def add_tag(request, article_id):
    if request.method =='POST':
        form = TagForm(request.POST)
        
        tag_request_from_browser = ''
        if form.is_valid():
            article_will_be_updated = Article.objects.get(pk=article_id)
            tag_request_from_browser = form.cleaned_data['tag_key'].split(':')
            tag_key = tag_request_from_browser[0]
            tag_value = 'http://www.wikidata.org/wiki/' + tag_request_from_browser[1]
            # tag = Tag(tag_key = form.cleaned_data['tag_key'],
            #         tag_value = form.cleaned_data['tag_value']
            #         )
            tag = Tag(tag_key = tag_key,
                    tag_value = tag_value
                )
            tag.save()
            tag.article.add(article_will_be_updated)
            return HttpResponseRedirect('/thanks')

    else:
        form = TagForm()

    return render(request, 'medicles/tag_create.html', {'form': form, 'article_id': article_id})                                                   

def ajax_load_tag(request):
    if request.is_ajax():
        tag_query = request.GET.get('tag_query', '')
        tags = Wikidata.get_tag_data(Wikidata, tag_query)

        data = {
            'tags': tags,
        }
        return JsonResponse(data)
