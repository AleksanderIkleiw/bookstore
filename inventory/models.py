from django.db import models
from bookstore.settings import MEDIA_ROOT
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


"""
By those 3 line of codes I am making email field required
"""


class Author(models.Model):
    name = models.CharField(max_length=25)  # defining charfield which is used to store shorter strings
    last_name = models.CharField(max_length=25)

    def __str__(self):  # when we see in admin panel or interpret object as a string, we will see the __str__ result
        return f"{self.name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateField(max_length=25)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    """
    We create relation with Author model. by using on_delete=models.CASCADE
    if the Author models get deleted, all book related object will also get deleted
    """
    quantity = models.IntegerField(default=0)  # default specifies default value
    photo = models.ImageField(upload_to=MEDIA_ROOT)  # specifies where to upload photos
    price = models.DecimalField(max_digits=4, decimal_places=2)  # specifies maximal number of digits and precision(decimal places)

    def __str__(self):
        return self.title


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    """
    ManyToManyField allows to have multiple books selected
    in the cart.
    """

    def __str__(self):
        return f"{self.user.username}'s Shopping Cart"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=25)
    content_of_order = models.TextField()

    def __str__(self):
        return f"{self.user}'s order of ID {self.order_id}"
