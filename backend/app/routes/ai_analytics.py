from fastapi import APIRouter, Depends, HTTPException

from app.schemas.ai_analytics import (
    AIAnalyticsRequest,
    AIAnalyticsResponse,
)
from app.utils.auth import get_authenticated_user
from app.utils.data_loader import get_full_dataset
from app.services.llm_service import (
    generate_analytics_query,
    generate_final_answer,
)
from app.services.ai_query_service import (
    execute_analytics_query,
)


# All AI Analytics endpoints are grouped
# Authentication is required for every endpoint in this router
router = APIRouter(
    prefix="/ai-analytics",
    tags=["AI Analytics"],
    dependencies=[
        Depends(get_authenticated_user)
    ],
)



@router.post(
    "/ask",
    response_model=AIAnalyticsResponse,
)
async def ask_ai_analytics(
    request: AIAnalyticsRequest,
    current_user: dict = Depends(
        get_authenticated_user
    ),
):

    
    try:
        # Load the dataset selected by the user
        # Only the logged in user can access the dataset because of user ID
        df = await get_full_dataset(
            dataset_id=request.dataset_id,
            user_id=current_user["id"],
        )



        # The AI cannot answer anything useful if the selected dataset does not exist or contains no records
        if df is None or df.empty:
            raise HTTPException(
                status_code=400,
                detail="The selected dataset is empty.",
            )



        # Convert the user's natural language question into a structured AnalyticsQuery.
        # The LLM decides what operation is needed, but it does not calculate the actual result
        query = generate_analytics_query(
            request.question,
            df,
        )

        # Execute the structured query using the backend.
        # Historical calculations are handled by Pandas, while forecast
        # requests are passed to the BusinessPulse forecasting models.
        result = await execute_analytics_query(
            df,
            query,
            dataset_id=request.dataset_id,
            user_id=current_user["id"],
        )

        # calculated result is translated into a short, natural language answer
        # The answer is generated from the result produced by the backend,
        # rather than allowing the LLM to invent or calculate values itself
        answer = generate_final_answer(
            request.question,
            query,
            result["data"],
        )

        # Return the original question, structured query, calculated result,
        # final answer, and the visualization type expected by the frontend
        return {
            "question": request.question,
            "query": query,
            "answer": answer,
            "result": result["data"],
            "visualization": result["type"],
        }

    # Preserve HTTP errors such as the empty dataset error above 
    except HTTPException:
        raise

    # Validation or query-processing errors are returned as client errors 
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    # Any unexpected failure is returned as a server error with the
    # original exception message to make debugging easier during development
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI analytics failed: {str(exc)}",
        )