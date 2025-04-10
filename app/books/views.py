import graphene

from app.books.models import Books
from app.books.schema import BooksType


class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType)

    #  get all books
    def resolve_all_books(root, info):
        return Books.objects.all()


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        excerpt = graphene.String(required=True)

    book = graphene.Field(BooksType)

    def mutate(self, info, title, excerpt):
        book = Books(title=title, excerpt=excerpt)
        book.save()
        return CreateBook(book=book)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
