from .models import Permission
from .models import Users
from django.shortcuts import redirect

def has_permission(request, module, action):
    user_role = Users.objects.get(user=request.user).role
    # SUPERADMIN BYPASS
    if user_role == "superadmin":
        return True
    permission = Permission.objects.filter(
        role=user_role,
        module=module
    ).first()
    # NO PERMISSION FOUND
    if not permission:
        return False
    # RETURN TRUE/FALSE
    return getattr(
        permission,
        action,
        False
    )

def permission_required(module, action):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not has_permission(
                request,
                module,
                action
            ):
                return redirect(
                    'no_access'
                )
            return view_func(
                request,
                *args,
                **kwargs
            )
        return wrapper
    return decorator