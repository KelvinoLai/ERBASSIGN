from django.db import models

# Create your models here.


class book(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    year = models.IntegerField()
    series = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    notes = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    reference = models.CharField(max_length=200)

    def __str__(self):
        return self.title
