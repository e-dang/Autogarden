from django.db import models

from django.contrib.auth.hashers import make_password


class TokenManager(models.Manager):
    def create(self, garden, uuid=None):
        hashed_uuid = make_password(uuid)
        token = self.model(garden=garden, uuid=hashed_uuid)
        token.save()
        return token
