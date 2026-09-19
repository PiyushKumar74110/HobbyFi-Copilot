from app.tools.user_tools import (
    get_users,
    search_user,
    get_trial_users,
)

from app.tools.revenue_tools import (
    get_revenue,
    get_total_revenue,
)

from app.tools.membership_tools import (
    get_membership,
    get_active_memberships,
    extend_trial,
)

from app.tools.analytics_tools import (
    get_analytics,
    get_new_users,
    get_active_users,
)

from app.tools.payment_tools import (
    get_payment_history,
    get_total_payment_by_user,
    get_last_payment,
)

from app.tools.user_tools import (
    get_users,
    search_user,
    get_trial_users,
    get_users_by_plan,
)


TOOL_REGISTRY = {

    "get_users": get_users,
    "search_user": search_user,
    "get_trial_users": get_trial_users,
    "get_users_by_plan": get_users_by_plan,

    "get_revenue": get_revenue,
    "get_total_revenue": get_total_revenue,

    "get_membership": get_membership,
    "get_active_memberships": get_active_memberships,
    "extend_trial": extend_trial,

    "get_analytics": get_analytics,
    "get_new_users": get_new_users,
    "get_active_users": get_active_users,

    "get_payment_history": get_payment_history,
    "get_total_payment_by_user": get_total_payment_by_user,
    "get_last_payment": get_last_payment,

}


def get_tool(
    tool_name: str,
):

    return TOOL_REGISTRY.get(
        tool_name
    )


def tool_exists(
    tool_name: str,
):

    return (
        tool_name in TOOL_REGISTRY
    )