WRITE_ACTIONS = {


    "extend_trial",


    "update_membership",


    "update_user",


    "delete_user"

}





def requires_approval(
    plan: dict
):


    """
    Check if the requested action
    modifies CRM data.
    """



    if not plan:


        return False



    tool_name = plan.get(
        "tool"
    )



    if tool_name in WRITE_ACTIONS:


        return True



    return False





def validate_plan(
    plan: dict
):


    """
    Validate AI generated plan
    before execution.
    """



    if not plan:


        return {


            "valid":
            False,


            "reason":
            "Empty plan"

        }



    if "type" not in plan:


        return {


            "valid":
            False,


            "reason":
            "Missing plan type"

        }





    if plan["type"] == "tool":


        if "tool" not in plan:


            return {


                "valid":
                False,


                "reason":
                "Missing tool name"

            }



    return {


        "valid":
        True

    }





def sanitize_response(
    response: str
):


    """
    Remove unwanted sensitive information
    before sending to vendor.
    """



    blocked_words = [

        "password",

        "secret_key",

        "token"

    ]



    for word in blocked_words:


        response = response.replace(

            word,

            "[hidden]"

        )



    return response