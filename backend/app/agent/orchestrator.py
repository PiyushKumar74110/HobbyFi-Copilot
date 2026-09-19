import json

from app.agent.planner import create_plan
from app.agent.executor import execute_plan

from app.llm.llm import generate

from app.security.guardrails import (
    requires_approval,
)

from app.services.approval_service import (
    create_approval_request,
)

from app.logs.logger import (
    log_info,
    log_error,
)

from app.services.audit_service import (
    record_query,
    record_plan,
    record_execution,
)

from app.services.response_formatter import (
    format_response,
)




def process_query(
    query: str,
    vendor_id: int | None = None,
    history=None,
):

    try:

        log_info(
            f"Processing query: {query}"
        )


        # -------------------------
        # Normalize History
        # -------------------------

        if history is None:

            history = []



        # -------------------------
        # Create Plan
        # -------------------------

        plan = create_plan(
            query,
            history=history,
        )
        print("PLAN:", plan)


        log_info(
            f"Generated plan: {plan}"
        )


        record_query(
            vendor_id,
            query,
        )



        # -------------------------
        # Validate Plan
        # -------------------------

        if not isinstance(
            plan,
            dict,
        ):

            return (
                "I could not understand the request."
            )



        record_plan(
            vendor_id,
            plan,
        )



        # -------------------------
        # Approval Check
        # -------------------------

        if requires_approval(plan):


            approval = create_approval_request(
                vendor_id=vendor_id,
                plan=plan,
            )


            # Validation failed

            if approval.get(
                "error"
            ):

                log_info(
                    "Approval validation failed: "
                    f"{approval['error']}"
                )

                return approval["error"]



            return json.dumps(
                {

                    "type":
                    "approval_required",


                    "approval_id":
                    approval["id"],


                    "message":
                    "This action requires your approval.",


                    "plan":
                    plan,


                    "preview":
                    approval.get(
                        "preview"
                    ),

                },

                default=str,

            )



        # -------------------------
        # Execute Plan
        # -------------------------
        print("CALLING EXECUTE_PLAN")
        
        execution_result = execute_plan(
                plan=plan,
                vendor_id=vendor_id,
        )

        print("EXECUTE_PLAN CALLED")


        log_info(
            f"Execution result: {execution_result}"
        )


        record_execution(
            vendor_id,
            execution_result,
        )



        # -------------------------
        # Handle Execution Error
        # -------------------------

        if execution_result.get(
            "error"
        ):

            return execution_result[
                "error"
            ]



        # -------------------------
        # Structured Response
        # -------------------------

        formatted_response = format_response(
            execution_result
        )


        if formatted_response:

            return formatted_response



        # -------------------------
        # Prepare Conversation History
        # -------------------------

        history_text = "\n".join(

            [

                f"{item['role']}: {item['content']}"

                for item in history

            ]

        )



        # -------------------------
        # Final LLM Response
        # -------------------------

        final_prompt = f"""
You are HobbyFi Copilot, an AI CRM assistant.

Answer the vendor clearly and concisely.

User Query:
{query}


Previous Conversation:
{history_text}


Execution Result:
{json.dumps(execution_result, default=str)}


Rules:

- Use only execution result for CRM facts.
- Use previous conversation only for context.
- Never invent users, revenue, memberships, or analytics.
- If data is unavailable, clearly say so.
- Do not mention internal tools, planner, database, or execution.
- Keep the answer natural and helpful.


Answer:
"""


        response = generate(
            final_prompt
        )


        return response.strip()



    except Exception as e:


        log_error(
            f"Orchestrator error: {str(e)}"
        )


        print(
            "ORCHESTRATOR ERROR:",
            repr(e),
        )


        return (
            f"ERROR: "
            f"{type(e).__name__}: "
            f"{str(e)}"
        )








