from pydantic import BaseModel
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from ai_agent import get_response_from_ai_agent

# Allowed models
ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile",
    "gpt-4o-mini"
]

# Request schema
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[Dict[str, str]]  # [{"role": "user", "content": "..."}]
    allow_search: bool


# Initialize app
app = FastAPI(title="LangGraph AI Agent API")


@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    Chat endpoint to interact with AI Agents built using LangGraph + LangChain.
    Dynamically selects model and provider.
    """
    try:
        if request.model_name not in ALLOWED_MODEL_NAMES:
            raise HTTPException(status_code=400, detail="Invalid model name. Please use a supported model.")

        # Extract user query (last message)
        query = request.messages[-1]["content"]
        llm_id = request.model_name
        provider = request.model_provider
        allow_search = request.allow_search
        system_prompt = request.system_prompt

        # Get AI response
        result = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)

        return {"status": "success", "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)
