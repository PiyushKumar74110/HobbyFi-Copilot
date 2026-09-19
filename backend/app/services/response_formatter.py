def format_response(
    execution_result: dict
):

    result = execution_result.get(
        "result"
    )


    if result is None:

        return None


    # -------------------------
    # Error / Message Response
    # -------------------------

    if isinstance(result, dict):

        if "error" in result:

            return result["error"]


        if (
            "message" in result
            and "users" not in result
        ):

            return result["message"]


    # -------------------------
    # Multiple Users Dictionary
    # -------------------------

    if (
        isinstance(result, dict)
        and "users" in result
    ):

        users = result["users"]


        if not users:

            return "No users found."


        response = (
            "Multiple users found. "
            "Please provide the complete CRM ID.\n\n"
        )


        for index, user in enumerate(
            users,
            start=1,
        ):

            response += (
                f"{index}. "
                f"Name: "
                f"{user.get('name', 'N/A')} | "
                f"CRM ID: "
                f"{user.get('crm_id', 'N/A')}"
                f"\n\n"
            )


        return response.strip()


    # -------------------------
    # Single User Dictionary
    # -------------------------

    if (
        isinstance(result, dict)
        and "crm_id" in result
        and "name" in result
    ):

        response = (
            "User Details\n\n"
            f"Name: "
            f"{result.get('name', 'N/A')}\n"
            f"CRM ID: "
            f"{result.get('crm_id', 'N/A')}\n"
            f"Email: "
            f"{result.get('email', 'N/A')}"
        )


        if result.get("phone"):

            response += (
                f"\nPhone: "
                f"{result.get('phone')}"
            )


        return response


    # -------------------------
    # List Response
    # -------------------------

    if isinstance(result, list):


        # Empty List

        if len(result) == 0:

            return "No records found."


        # -------------------------
        # Single User In List
        # -------------------------

        if (
            len(result) == 1
            and isinstance(
                result[0],
                dict,
            )
            and "crm_id" in result[0]
            and "name" in result[0]
        ):

            user = result[0]


            response = (
                "User Details\n\n"
                f"Name: "
                f"{user.get('name', 'N/A')}\n"
                f"CRM ID: "
                f"{user.get('crm_id', 'N/A')}\n"
                f"Email: "
                f"{user.get('email', 'N/A')}"
            )


            if user.get("phone"):

                response += (
                    f"\nPhone: "
                    f"{user.get('phone')}"
                )


            return response


        # -------------------------
        # Multiple List Records
        # -------------------------

        response = ""


        for index, item in enumerate(
            result,
            start=1,
        ):

            response += (
                f"{index}. "
            )


            if isinstance(item, dict):

                fields = []


                for key, value in item.items():

                    formatted_key = (
                        key
                        .replace("_", " ")
                        .title()
                    )


                    fields.append(
                        f"{formatted_key}: "
                        f"{value}"
                    )


                response += (
                    " | ".join(fields)
                )

            else:

                response += str(item)


            response += "\n\n"


        return response.strip()


    # -------------------------
    # Generic Dictionary
    # -------------------------

    if isinstance(result, dict):

        response = ""


        for key, value in result.items():

            formatted_key = (
                key
                .replace("_", " ")
                .title()
            )


            response += (
                f"{formatted_key}: "
                f"{value}\n"
            )


        return response.strip()


    # -------------------------
    # Unsupported Result
    # -------------------------

    return None