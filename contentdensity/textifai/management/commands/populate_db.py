from django.core.management.base import BaseCommand
from textifai.models import User

class Command(BaseCommand):
    args = '<>'
    help = 'Run this script to populate database w/ sample users.'

    def create_users(self):
        user = User(username='tom',,email='tomthebomb@hotmail.com')
        user.save()

    def handle(self, *args, **options):
        self.create_users()