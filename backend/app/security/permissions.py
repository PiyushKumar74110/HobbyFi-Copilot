from enum import Enum



class Permission(str, Enum):

    VIEW_USERS = "view_users"

    VIEW_REVENUE = "view_revenue"

    VIEW_ANALYTICS = "view_analytics"

    UPDATE_MEMBERSHIP = "update_membership"

    UPDATE_USER = "update_user"



# Temporary permission mapping
# Later connect with database roles


ROLE_PERMISSIONS = {


    "vendor": [

        Permission.VIEW_USERS,

        Permission.VIEW_REVENUE,

        Permission.VIEW_ANALYTICS,

        Permission.UPDATE_MEMBERSHIP

    ],


    "admin": [

        Permission.VIEW_USERS,

        Permission.VIEW_REVENUE,

        Permission.VIEW_ANALYTICS,

        Permission.UPDATE_MEMBERSHIP,

        Permission.UPDATE_USER

    ]

}




def check_permission(
    role: str,
    permission: Permission
):


    allowed_permissions = ROLE_PERMISSIONS.get(
        role,
        []
    )


    return permission in allowed_permissions