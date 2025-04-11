from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from app.books.models import Books


class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "excerpt")


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")
