from django.core.management.base import BaseCommand
from oauth2_provider.models import Application, generate_client_secret, generate_client_id

from e_commerce.models import User

from utility.env_setup import environment


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Initializing super admin started...")

        superUsers = User.objects.filter(is_superuser=True)
        if superUsers.count() == 0:
            user=User.objects.create_superuser(
                username=environment.DJANGO_SUPERUSER_USERNAME,
                password=environment.DJANGO_SUPERUSER_PASSWORD,
                email=environment.DJANGO_SUPERUSER_EMAIL,
                phone=environment.DJANGO_SUPERUSER_PHONE,
                is_superuser=True,
                is_staff=True,
            )
            self.create_app(user)
            print("SuperUser created successfully.")
        else:
            print("SuperUser already exists.")

    def create_app(self, user):
        application = Application(
            name="Trade_Admin_App",
            client_id=generate_client_id(),
            client_secret=generate_client_secret(),
            client_type="confidential",
            authorization_grant_type="password",
            user_id=user.id
        )
        application.save()
        print("OAuth Application created successfully.")
        return application