from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperAdmin(BasePermission):
    """
    Custom permission to only allow superusers (superadmins) to access the endpoint.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_staff
                or request.user.role == "superadmin"
            )
        )


class RoleBasedPermission(BasePermission):
    """
    Custom permission for role-based access control:
    - Superadmin (is_staff/is_superuser or role == 'superadmin') can do anything.
    - Viewer (role == 'viewer') can only view data (GET, HEAD, OPTIONS).
    - Data Enumerator (role == 'data_enumerator') and Field Coordinator (role == 'field_coordinator')
      can view (GET, HEAD, OPTIONS) and upload (POST). They cannot modify or delete.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False

        # Superadmin can do anything
        if user.role == "superadmin" or user.is_staff or user.is_superuser:
            return True

        # Viewer can only view
        if user.role == "viewer":
            return request.method in SAFE_METHODS

        # Data Enumerator and Field Coordinator can view and upload (POST)
        if user.role in ("data_enumerator", "field_coordinator"):
            return request.method in SAFE_METHODS or request.method == "POST"

        return False
