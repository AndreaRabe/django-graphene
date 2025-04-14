import graphene
from django.conf import settings
from django.core.mail import send_mail

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
        # authorization
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be connected to perform this action")
        if user.role != "hr":
            raise Exception("You must be Hr Advisor to perform this action")

        user_data = User.objects.get(pk=user)

        notification = Notification(user=user_data, title=title, text=text)
        notification.save()

        # Envoi automatique de l'email
        send_mail(
            subject=title,
            message=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_data.email],
            fail_silently=False,  # ou True si tu veux éviter les exceptions
        )

        return CreateNotification(notification=notification)


class NotificationMutation(graphene.ObjectType):
    create_notification = CreateNotification.Field()
