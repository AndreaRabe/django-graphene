import graphene
import graphql_jwt

from app.books.models import Books
from app.books.schema import BooksType


# Views for user
# class RegisterUser(graphene.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         email = graphene.String()
#         password = graphene.String(required=True)
#
#     user = graphene.Field(UserType)
#
#     def mutate(self, info, username, email=None, password=None):
#         if User.objects.filter(username=username).exists():
#             raise Exception("Ce nom d'utilisateur est déjà pris")
#
#         user = User(username=username, email=email)
#         user.set_password(password)
#         user.save()
#
#         return RegisterUser(user=user)


# Views for books
class BooksQuery(graphene.ObjectType):
    all_books = graphene.List(BooksType)

    search_books = graphene.List(BooksType, title=graphene.String(required=True))

    #  get all books
    def resolve_all_books(root, info):
        return Books.objects.all()

    def resolve_search_books(root, info, title):
        return Books.objects.filter(title__icontains=title)


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        excerpt = graphene.String(required=True)

    book = graphene.Field(BooksType)

    def mutate(self, info, title, excerpt):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Vous devez être connecté pour créer un livre.")
        book = Books(title=title, excerpt=excerpt)
        book.save()
        return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        excerpt = graphene.String()

    book = graphene.Field(BooksType)

    def mutate(self, info, id, title=None, excerpt=None):
        try:
            book = Books.objects.get(pk=id)
        except Books.DoesNotExist:
            raise Exception("Book not found")

        if title is not None:
            book.title = title
        if excerpt is not None:
            book.excerpt = excerpt

        book.save()
        return UpdateBook(book=book)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    book = graphene.Field(BooksType)

    def mutate(self, info, id):
        try:
            book = Books.objects.get(pk=id)
        except Books.DoesNotExist:
            raise Exception("Book not found")

        book.delete()
        return DeleteBook(ok=True, book=book)


class Mutation(graphene.ObjectType):
    # register_user = RegisterUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

# schema = graphene.Schema(query=Query, mutation=Mutation)
