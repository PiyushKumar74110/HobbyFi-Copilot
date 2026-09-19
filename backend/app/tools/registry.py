from app.tools.user_tools import (
    get_users,
    search_user,
    get_trial_users,
    get_users_by_plan
)


from app.tools.revenue_tools import (
    get_revenue,
    get_total_revenue,
    get_revenue_by_date

)


from app.tools.membership_tools import (
    get_membership,
    get_active_memberships,
    extend_trial
)


from app.tools.analytics_tools import (
    total_users,
    new_users_this_month,
    active_memberships,
    expired_memberships,
    revenue_this_month,
    revenue_last_30_days,
    average_payment,
    top_membership_plans,
    dashboard_summary
)

from app.tools.payment_tools import (
    create_payment,
    get_payment,
    list_payments,
    list_user_payments,
    update_payment_amount,
    delete_payment,
    total_revenue,
    latest_payment
)





# Central Tool Registry

TOOLS = {


    # User Tools

    "get_users":
    get_users,


    "search_user":
    search_user,


    "get_trial_users":
    get_trial_users,

    "get_users_by_plan":
get_users_by_plan,



    # Revenue Tools

    "get_revenue":
    get_revenue,


    "get_total_revenue":
    get_total_revenue,

    "get_revenue_by_date" : 
    get_revenue_by_date,



    # Membership Tools

    "get_membership":
    get_membership,


    "get_active_memberships":
    get_active_memberships,


    "extend_trial":
    extend_trial,



    # Analytics Tools

    "total_users" : total_users,
    "new_users_this_month" : new_users_this_month ,
    "active_memberships" : active_memberships,
    "expired_memberships" : expired_memberships,
    "revenue_this_month" : revenue_this_month,
    "revenue_last_30_days" : revenue_last_30_days,
    "average_payment" : average_payment,
    "top_membership_plans" : top_membership_plans,
    "dashboard_summary" : dashboard_summary,

    # Payment Tools

    "create_payment" : create_payment,
    "get_payment" : get_payment,
    "list_payments" : list_payments,
    "list_user_payments" : list_user_payments,
    "update_payment_amount" : update_payment_amount,
    "delete_payment" : delete_payment,
    "total_revenue" : total_revenue,
    "latest_payment" : latest_payment

}





def get_tool(
    tool_name: str
):


    return TOOLS.get(
        tool_name
    )





def list_tools():

    return list(
        TOOLS.keys()
    )