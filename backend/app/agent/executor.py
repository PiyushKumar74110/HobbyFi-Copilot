from app.tools.registry import (
    get_tool
)


from app.rag.retriever import (
    retrieve_context
)


from app.logs.logger import (
    log_info,
    log_error
)






def execute_plan(
    plan: dict,
    vendor_id: int | None = None,
):    


    try:


        plan_type = plan.get(
            "type"
        )



        # -------------------------
        # RAG Execution
        # -------------------------


        if plan_type == "rag":


            query = plan.get(
                "query"
            )


            log_info(

                f"RAG query: {query}"

            )



            context = retrieve_context(
                query
            )



            return {


                "type":
                "rag",


                "context":
                context

            }





        # -------------------------
        # Tool Execution
        # -------------------------


        if plan_type == "tool":


            tool_name = plan.get(
                "tool"
            )


            tool_input = plan.get(
                "query"
            )



            log_info(

                f"Executing tool: {tool_name}"

            )



            tool = get_tool(
                tool_name
            )



            if not tool:


                return {


                    "error":
                    f"Tool {tool_name} not found"

                }





            # Supports both: String Input and Dictionary Input

            
            print("=" * 50)
            print("TOOL NAME:", tool_name)
            print("TOOL INPUT:", tool_input)
            print("=" * 50)


            

            # Attach authenticated vendor_id

            if isinstance(tool_input, dict):

                if vendor_id is not None:
                    tool_input["vendor_id"] = vendor_id

            else:

                tool_input = {
                    "query": tool_input,
                    "vendor_id": vendor_id,
                }

            result = tool(tool_input)



            return {


                "type":
                "tool",


                "tool":
                tool_name,


                "result":
                result

            }





        return {


            "error":
            "Unknown plan type"

        }





    except Exception as e:


        log_error(

            f"Executor error: {str(e)}"

        )


        return {


            "error":
            str(e)

        }