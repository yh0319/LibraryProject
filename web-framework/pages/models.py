from django.db import models

class Books(models.Model):
    bCode = models.IntegerField(primary_key=True)
    bName = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    classno = models.IntegerField()
    loanCnt = models.IntegerField()
    bImage = models.CharField(max_length=255)

