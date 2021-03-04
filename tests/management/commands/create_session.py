from django.conf import settings
from django.contrib.auth import (BACKEND_SESSION_KEY, SESSION_KEY, HASH_SESSION_KEY,
                                 get_user_model)
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('password')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options['email'], options['password'])
        self.stdout.write(session_key)


def create_pre_authenticated_session(email: str, password: str) -> str:
    user = User.objects.create_user(email=email, password=password)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session.session_key


def create_authenticated_session(user: User) -> str:
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session.session_key
