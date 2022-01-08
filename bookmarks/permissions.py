from rest_framework import permissions

class BookmarkPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, bookmark):
        if not bookmark.private:
            return True
        elif bookmark.owner.id == request.user.id:
            return True
        return False