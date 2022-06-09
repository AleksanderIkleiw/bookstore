import json

from django.shortcuts import render, redirect
from .models import Book
from .models import ShoppingCart, Order
from django.contrib.auth.models import User
from django.contrib import messages
from bookstore.settings import PAYPAL_CLIENT_ID
from login_system.send_mail import send__email
from django.contrib.auth.decorators import login_required


def home_view(request):
    """

    :param request: user's request
    :return: render home.html template, pass request and book objects, and bool value whether there are any books
    """
    objects_expanded = [build_dict(x) for x in Book.objects.all()]
    """
    # we use a function that ,,builds'' dictionary for all book objects, so they can be displayed on the home page
    """
    return render(request, 'inventory/home.html', {'Objects': objects_expanded,
                                                   'Is_empty': not bool(objects_expanded)})


@login_required
def buy_view(request, object_id):
    """
    login_required is a decorator that requires user to be logged in in order
    to access the view. If they aren't logged in, they are redirected to the
    logging view
    """
    user = User.objects.get(pk=request.user.pk)  # calling specific user object by their primary key from request
    cart = ShoppingCart.objects.get_or_create(user=user)[0]
    """
    gets or create cart. [0] is used, because the second element in list is bool value whether cart exists
    """
    book = Book.objects.get(id=object_id)
    if book in cart.books.all():  # checks if user has already added the same book to cart
        messages.error(request, 'Item is already in the cart.')
        return redirect('home_page')  # redirects to the home_page(name comes from urls name keyword)
    if getattr(book, 'quantity') < 1:  # checks if there are enough books to sell
        messages.error(request, 'Item is out of stock.')  # messages error allows to render any ,,alert'' in the next view
        return redirect('home_page')
    cart.books.add(book)  # adding specified book object to cart
    messages.success(request, 'Item added to cart successfully.')
    return redirect('home_page')


@login_required
def checkout_view(request):
    user = User.objects.get(pk=request.user.pk)
    cart = ShoppingCart.objects.get_or_create(user=user)[0]
    books_expanded = [build_dict(x) for x in cart.books.all()]
    cart_books = [x['title'] for x in books_expanded]  # list comprehension to get all book titles
    for book_title in cart_books:
        book = Book.objects.get(title=book_title)
        if getattr(book, 'quantity') < 1:
            """
            checks if there are enough book. If not, whole cart is wiped and user is redirected to home page
            """
            clear_shopping_cart(cart)
            messages.error(request, 'One or more items in your shopping cart were out of stock. Please add your items again.')

            return redirect('home_page')

    """
    for below return: user_pk is user primary key, api key is paypal's api key, total_price is sum
    of all books in cart and then it is passed to paypal's api
    """
    return render(request, 'inventory/checkout.html', {'Books': books_expanded,
                                                       'Total_Price': sum([x['price'] for x in books_expanded]),
                                                       'Is_Empty': not bool(books_expanded),
                                                       'User_pk': user.pk,
                                                       'Api_key': PAYPAL_CLIENT_ID})


@login_required
def complete_view(request):
    body = json.loads(request.body)  # retrieve JS fetch body
    body_data = body['data_']

    user = User.objects.get(pk=request.user.pk)
    cart = ShoppingCart.objects.get(user=user)

    user_pk = body['user_primary_key']
    order_id = body_data['id']
    titles_of_the_order_books = [getattr(x, 'title') for x in cart.books.all()]  # getting titles from all books from cart
    ids_of_the_order_books = [getattr(x, 'id') for x in cart.books.all()]
    order_content = '| '.join(titles_of_the_order_books)
    """
    each book title is joined with ,,|'' to display whole order's content in one string
    """
    status = body_data['status']

    if status == 'COMPLETED':  # if paypal's api confirmed that the payment has been completed
        messages.success(request, 'Book has been successfully bought.')

    """
    creation of order object that is saved to the database
    """

    order_obj = Order.objects.create(user=user)
    order_obj.order_id = order_id
    order_obj.content_of_order = order_content
    order_obj.save()

    clear_shopping_cart(cart)  # clearing user's shopping cart

    """
    after purchase is complete, we subtract 1 quantity of each bought book
    """

    for book_id in ids_of_the_order_books:
        book_obj = Book.objects.get(id=book_id)
        book_obj.quantity -= 1
        book_obj.save()

    mail_body = f'Thank you for buying {order_content} books. Your order ID is {order_id}'
    subject = 'Confirmation of purchase'
    send__email(getattr(user, 'email'), subject, mail_body)
    """
    we call function to send mail and we get receiver mail from the user model
    """

    return redirect('home_page')


@login_required
def bought_view(request):  # function to redirect to home_page with message
    messages.success(request, 'Book has been successfully bought')
    return redirect('home_page')


@login_required
def remove_from_cart_view(request, book_id):  # function that allows user to remove book from cart
    user = User.objects.get(pk=request.user.pk)
    cart = ShoppingCart.objects.get(user=user)
    cart.books.remove(book_id)  # function that actually remove book
    messages.success(request, 'Book has been successfully removed.')
    return redirect('checkout_page')


def build_dict(obj):
    temp = {}
    fields = [field.name for field in obj._meta.get_fields()]
    """
    list comprehension that gets all fields of model. we remove shoppingcart field, because
    it is ,,hidden'' field due to relation
    """
    fields.remove('shoppingcart')
    for field in fields:
        temp[field] = getattr(obj, field)
    """
    by this simple for loop we build dictionary for each object with their models field and value
    """
    return temp


def clear_shopping_cart(cart):  # deletes whole user's cart object
    cart.delete()
    cart.save()
