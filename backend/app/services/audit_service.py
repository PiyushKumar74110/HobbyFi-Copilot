from datetime import datetime


from app.logs.audit_logger import (
    audit_log
)





def record_query(
    vendor_id: int,
    query: str
):


    event = {


        "event":
        "USER_QUERY",


        "vendor_id":
        vendor_id,


        "query":
        query,


        "timestamp":
        datetime.utcnow()

    }



    audit_log(

        "USER_QUERY",

        event

    )



    return event





def record_plan(
    vendor_id: int,
    plan: dict
):


    event = {


        "event":
        "AI_PLAN_CREATED",


        "vendor_id":
        vendor_id,


        "plan":
        plan,


        "timestamp":
        datetime.utcnow()

    }



    audit_log(

        "AI_PLAN_CREATED",

        event

    )



    return event





def record_execution(
    tool_name: str,
    result
):


    event = {


        "event":
        "TOOL_EXECUTION",


        "tool":
        tool_name,


        "result":
        result,


        "timestamp":
        datetime.utcnow()

    }



    audit_log(

        "TOOL_EXECUTION",

        event

    )



    return event





def record_database_change(
    action: str,
    data: dict
):


    event = {


        "event":
        "DATABASE_CHANGE",


        "action":
        action,


        "data":
        data,


        "timestamp":
        datetime.utcnow()

    }



    audit_log(

        "DATABASE_CHANGE",

        event

    )



    return event