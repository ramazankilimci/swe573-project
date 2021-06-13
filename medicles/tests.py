from datetime import datetime
from django.http import response
from django.test import TestCase, Client
from .models import Article, Tag
from medicles import services
import datetime
from django.urls import reverse
# Create your tests here.

class ViewTests(TestCase):
    
    # Test Index Page
    def test_index_page_accessed_successfully(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200 )

    # Test Search Page
    def test_search_page_accessed_successfully(self):
        c = Client()
        response = c.get('/search')
        self.assertEqual(response.status_code, 301)

    # Test Admin Page
    def test_admin_page_accessed_successfully(self):
        c = Client()
        response = c.get('/admin')
        self.assertEqual(response.status_code, 301)

class ServiceTests(TestCase):

    # Test PubMed ESearch API Article ID function
    def test_esearch_get_article_id_is_successful(self):
        srv_obj = services
        term = 'covid'
        retmax = 10
        response = srv_obj.get_article_ids(term, retmax)
        self.assertEqual(len(response), retmax)

    def test_efetch_get_article_detail_is_successful(self):
        srv_obj = services
        term = 'covid'
        retmax = 50
        retmax_iter = 25
        response = srv_obj.get_articles_with_details(term, retmax, retmax_iter)
        self.assertGreaterEqual(len(response), retmax_iter)

    def test_create_db_records_is_successful(self):
        srv_obj = services
        term = 'covid'
        retmax = 50
        retmax_iter = 25
        response = srv_obj.create_db(term, retmax, retmax_iter)
        self.assertAlmostEquals(len(response), retmax, delta=10)
        
class ArticleTests(TestCase):
    @classmethod
    def setUpArticleTestClassData(cls):
        single_article_list = []
        article_id = 1
        pub_date = datetime.datetime(2021, 8, 21)
        article_title = "Test for article title"
        article_abstract = "Test for article abstract"
        author_list = "Test for author list"
        keyword_list = "Keyword"
        for i in range(2):
            row_article_list = [article_id,
                                pub_date,
                                article_title,
                                article_abstract,
                                author_list,
                                keyword_list,
                                ]
            single_article_list.append(row_article_list)
            article_id +=1
        return single_article_list

    def test_single_insert_to_db_successful(self):
        single_article_list = ArticleTests.setUpArticleTestClassData()
        article = Article.objects.create(article_id = single_article_list[0][0],
                            pub_date = single_article_list[0][1],
                            article_title = single_article_list[0][2],
                            article_abstract = single_article_list[0][3],
                            author_list = single_article_list[0][4],
                            keyword_list = single_article_list[0][5]
                            )
        print(article)
        self.assertEqual(article.article_id, 1)

    def test_multiple_insert_to_db_successful(self):
        single_article_list = ArticleTests.setUpArticleTestClassData()
        for i in range(len(single_article_list)):
            article = Article.objects.create(article_id = single_article_list[i][0],
                                pub_date = single_article_list[i][1],
                                article_title = single_article_list[i][2],
                                article_abstract = single_article_list[i][3],
                                author_list = single_article_list[i][4],
                                keyword_list = single_article_list[i][5]
                                )
            print(article)
        count = Article.objects.all().count()
        self.assertEqual(count, len(single_article_list))