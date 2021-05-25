import os
import requests
import xml.etree.ElementTree as ET
from .models import Article
import datetime

def get_article_ids():
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=post+traumatic+stress+disorder+AND&retmode=json&retmax=10"

    payload={}
    headers = {
        'Cookie': 'ncbi_sid=E951A4FF8F247310_DA2ESID'
        }

    response = requests.request("GET", url, headers=headers, data=payload)
    articles = response.json()
    #print(len(articles['esearchresult']['idlist']))
    article_list = []
    for i in range(len(articles['esearchresult']['idlist'])):
        article_list.append(articles['esearchresult']['idlist'][i])
    return article_list

#print(get_article_ids())

def get_article_detail():
    articles = get_article_ids()
    article_list = []
    for i in range(len(articles)):    

        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id="+articles[i]+"&retmode=json"

        payload={}
        headers = {
            'Cookie': 'ncbi_sid=E951A4FF8F247310_DA2ESID'
            }

        response = requests.request("GET", url, headers=headers, data=payload)
        article_detail = response.json()

        # Convert str to datetime format.
        pub_date = article_detail['result'][articles[i]]['history'][0]['date']
        pub_date = datetime.datetime.strptime(pub_date, '%Y/%m/%d %H:%M')
        article_list.append(
            [articles[i],
            pub_date,
            article_detail['result'][articles[i]]['title']])
    return article_list

#print(get_article_detail())

def get_article_abstract():
    articles = get_article_detail()
    for i in range(len(articles)):

        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+articles[i][0]+"&rettype=abstract"
        #print(url)
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        
        abs_tree = ET.fromstring(response.content)
        article_abstract = ""
        for abstract in abs_tree.iter('AbstractText'):
            article_abstract += abstract.text
        #print(article_abstract)
        #print('-------------')

        articles_nested_list = articles[i]
        articles_nested_list.append(article_abstract)

    return articles

#print(get_article_abstract())


def create_db():
    articles = get_article_abstract()
    for i in range(len(articles)):
        Article.objects.create(article_id = articles[i][0],
        pub_date = articles[i][1],
        article_title = articles[i][2],
        article_abstract = articles[i][3],
        )

    query_result = Article.objects.all()

    return query_result

#print(create_db())


def update_db():
    latest_article_id = Article.objects.latest('article_id').article_id
    new_articles = get_article_abstract()
    for i in range(len(new_articles)):
        if int(new_articles[i][0]) > latest_article_id:
            Article.objects.create(article_id = new_articles[i][0],
            pub_date = new_articles[i][1],
            article_title = new_articles[i][2],
            article_abstract = new_articles[i][3],
            )
    
    query_result = Article.objects.all()
    return query_result

#update_db()


# from medicles.models import Article 
# from medicles import services 
# db = services 
# db.get_articles_from_db() 

