from django.db import models

# Create your models here.
class books(models.Model):
    bCode = models.AutoField(primary_key=True)
    bName = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    classno = models.IntegerField()
    loanCnt = models.IntegerField()
    bImage = models.CharField(max_length=255)

class classno(models.Model):
    classno = models.IntegerField()
    cName = models.CharField(max_length=45)

class members(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    email = models.CharField(max_length=255)
    birth = models.IntegerField()
    mName = models.CharField(max_length=20)
    sex = models.CharField(max_length=1)
    passwd = models.CharField(max_length=20)


class loan(models.Model):
    lCode = models.AutoField(primary_key=True)
    id = models.ForeignKey(members, on_delete=models.CASCADE)
    bName = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    bImage = models.CharField(max_length=255)

    def __str__(self):
        return self.id

class recommendations(models.Model):
    rCode = models.AutoField(primary_key=True)
    id = models.ForeignKey(members, on_delete=models.CASCADE)
    bName = models.CharField(max_length=255)
    bImage = models.CharField(max_length=255)

    def __str__(self):
        return self.id


