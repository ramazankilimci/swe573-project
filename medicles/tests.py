from datetime import datetime
from django.test import TestCase
from .models import Article
import datetime
from django.urls import reverse
# Create your tests here.

class ArticleTests(TestCase):
    
    def setUp(self):
        url = reverse('search')
        self.response = self.client.get(url)

    def search_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'medicles/search_results.html')
