from django.db import models

# Create your models here.

# Article will be filled Entrez API information.

class Article(models.Model):
    article_id = models.BigIntegerField()
    pub_date = models.DateTimeField()
    article_title = models.TextField()
    article_abstract = models.TextField()

    def __str__(self):
        return str(self.article_id)



