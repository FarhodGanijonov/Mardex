from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Faqat profil egasi o'z p    rofilini tahrir qila oladi.
    Boshqalar faqat ko'rish huquqiga ega.
    """
    def has_object_permission(self, request, view, obj):
        # O'qish uchun ruxsat
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return obj.user == request.user


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'
