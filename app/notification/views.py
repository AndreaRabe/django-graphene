import graphene

from app.notification.models import Notification
from app.notification.schema import NotificationType
from app.users.models import User


class NotificationQuery(graphene.ObjectType):
    all_notifications = graphene.List(NotificationType)

    def resolve_all_notifications(root, info):
        return Notification.objects.all()


class CreateNotification(graphene.Mutation):
    class Arguments:
        user = graphene.ID(required=True)
        title = graphene.String(required=True)
        text = graphene.String(required=True)

    notification = graphene.Field(NotificationType)

    def mutate(self, info, user, title, text):
        user_data = User.objects.get(pk=user)

        notification = Notification(user=user_data, title=title, text=text)
        notification.save()

        return CreateNotification(notification=notification)


class NotificationMutation(graphene.ObjectType):
    create_notification = CreateNotification.Field()
