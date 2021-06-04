from django.db import models
from medicles.managers import ArticleManager

from django.contrib.postgres.search import SearchVector, SearchVectorField



# Create your models here.

# Article will be filled Entrez API information.

class Article(models.Model):
    #article_id = models.BigIntegerField()
    article_id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField()
    article_title = models.TextField(blank=True, null=True)
    article_abstract = models.TextField(blank=True, null=True)
    author_list = models.TextField(blank=True, null=True)
    keyword_list = models.TextField(blank=True, null=True)
    search_vector = SearchVectorField(null=True, )

    objects = ArticleManager()

    def __str__(self):
        return str(self.article_id)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Article.objects.update(search_vector = (
            SearchVector('article_abstract', weight = 'A')
            + SearchVector('keyword_list', weight = 'B')
            )
        ) 



