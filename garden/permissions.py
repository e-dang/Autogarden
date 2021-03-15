from rest_framework.permissions import BasePermission


class TokenPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        token = self._get_token(request.META.get('HTTP_AUTHORIZATION'))
        if obj.token.verify(token):
            return True
        return False

    def _get_token(self, auth_header):
        if auth_header is None:
            return None
        return auth_header.split(' ')[-1]
