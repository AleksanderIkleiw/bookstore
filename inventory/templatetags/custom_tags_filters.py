from django.template.defaulttags import register
from django import template
from bookstore.settings import MEDIA_URL

reg = template.Library() # we have to register module as a template library


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


"""
simple filter to retrieve dictionary's value
"""


@register.filter
def create_photo_url(file_name):
    return MEDIA_URL + file_name.name


"""
filter to create url out of MEDIA_URL and file_name
"""