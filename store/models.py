from django.db import models


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField()
    photo = models.ImageField(upload_to='authors_photos/', null=True, blank=True)


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField()

