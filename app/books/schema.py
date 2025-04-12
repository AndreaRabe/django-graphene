from graphene_django import DjangoObjectType

from app.books.models import Books


class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "excerpt")
