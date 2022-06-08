from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateField(max_length=25)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title
