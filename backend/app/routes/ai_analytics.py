# import time


# from fastapi import APIRouter, Depends, HTTPException

# from app.schemas.ai_analytics import (
#     AIAnalyticsRequest,
#     AIAnalyticsResponse,
# )
# from app.utils.auth import get_authenticated_user
# from app.utils.data_loader import get_full_dataset
# from app.services.llm_service import (
#     generate_agent_plan,
#     generate_final_answer,
# )
# from app.services.ai_query_service import execute_agent_plan


# router = APIRouter(
#     prefix="/ai-analytics",
#     tags=["AI Analytics"],
# )


# @router.post(
#     "/ask",
#     response_model=AIAnalyticsResponse,
# )
# async def ask_ai_analytics(
#     request: AIAnalyticsRequest,
#     current_user: dict = Depends(get_authenticated_user),
# ):
#     try:

#         request_start = time.perf_counter()
#         df = await get_full_dataset(
#             dataset_id=request.dataset_id,
#             user_id=current_user["id"],
#         )

#         if df is None or df.empty:
#             raise HTTPException(
#                 status_code=400,
#                 detail="The selected dataset is empty.",
#             )

#         plan = generate_agent_plan(
#             request.question,
#             df,
#         )

#         # General questions should be answered normally
#         # instead of returning the old BusinessPulse-only message.
#         if plan.tool == "general_tool":
#             answer = generate_final_answer(
#                 request.question,
#                 plan.query,
#                 None,
#             )

#             return {
#                 "question": request.question,
#                 "query": plan.query,
#                 "answer": answer,
#                 "result": None,
#                 "visualization": "text",
#                 "table_data": None,
#                 "chart_data": None,
#             }

#         # Execute the selected BusinessPulse tool.
#         result = await execute_agent_plan(
#             df,
#             plan,
#             dataset_id=request.dataset_id,
#             user_id=current_user["id"],
#             question=request.question,
#         )

#         # Convert the verified backend result into the final answer.
#         answer = generate_final_answer(
#             request.question,
#             plan.query,
#             result["data"],
#         )

#         return {
#             "question": request.question,
#             "query": plan.query,
#             "answer": answer,
#             "result": result["data"],
#             "visualization": result["type"],
#             "table_data": result.get("table_data"),
#             "chart_data": result.get("chart_data"),
#         }


#     except HTTPException:
#         raise

#     except ValueError as exc:
#         raise HTTPException(
#             status_code=400,
#             detail=str(exc),
#         )

#     except Exception as exc:
#         raise HTTPException(
#             status_code=500,
#             detail=f"AI analytics failed: {str(exc)}",
#         )


import time

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.ai_analytics import (
    AIAnalyticsRequest,
    AIAnalyticsResponse,
)
from app.utils.auth import get_authenticated_user
from app.utils.data_loader import get_full_dataset
from app.services.llm_service import (
    generate_agent_plan,
    generate_final_answer,
)
from app.services.ai_query_service import execute_agent_plan

router = APIRouter(
    prefix="/ai-analytics",
    tags=["AI Analytics"],
)


@router.post(
    "/ask",
    response_model=AIAnalyticsResponse,
)
async def ask_ai_analytics(
    request: AIAnalyticsRequest,
    current_user: dict = Depends(get_authenticated_user),
):
    try:
        request_start = time.perf_counter()

        dataset_start = time.perf_counter()

        df = await get_full_dataset(
            dataset_id=request.dataset_id,
            user_id=current_user["id"],
        )

        print(
            f"[AI TIMING] Dataset load: " f"{time.perf_counter() - dataset_start:.2f}s"
        )

        if df is None or df.empty:
            raise HTTPException(
                status_code=400,
                detail="The selected dataset is empty.",
            )

        plan = generate_agent_plan(
            request.question,
            df,
        )

        # General questions should be answered normally
        # instead of using the BusinessPulse dataset executor.
        if plan.tool == "general_tool":
            answer = generate_final_answer(
                request.question,
                plan.query,
                None,
            )

            print(
                f"[AI TIMING] Total request: "
                f"{time.perf_counter() - request_start:.2f}s"
            )

            return {
                "question": request.question,
                "query": plan.query,
                "answer": answer,
                "result": None,
                "visualization": "text",
                "table_data": None,
                "chart_data": None,
            }

        # Execute the selected BusinessPulse tool.
        execution_start = time.perf_counter()

        result = await execute_agent_plan(
            df,
            plan,
            dataset_id=request.dataset_id,
            user_id=current_user["id"],
            question=request.question,
        )

        print(
            f"[AI TIMING] Tool execution: "
            f"{time.perf_counter() - execution_start:.2f}s"
        )

        # Convert the verified backend result into the final answer.
        answer = generate_final_answer(
            request.question,
            plan.query,
            result["data"],
        )

        print(
            f"[AI TIMING] Total request: " f"{time.perf_counter() - request_start:.2f}s"
        )

        return {
            "question": request.question,
            "query": plan.query,
            "answer": answer,
            "result": result["data"],
            "visualization": result["type"],
            "table_data": result.get("table_data"),
            "chart_data": result.get("chart_data"),
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI analytics failed: {str(exc)}",
        )
