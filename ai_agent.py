from dotenv import load_dotenv
import os

load_dotenv()

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    """
    Create a LangGraph AI Agent using Groq or OpenAI, optionally with Tavily search.
    """

    # Select model provider
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id)
    else:
        raise ValueError("Invalid provider. Use 'Groq' or 'OpenAI'.")

    # Add optional search tool
    tools = [TavilySearch(max_results=2)] if allow_search else []

    # Create agent (React-style agent)
    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # Build message history for the agent
    state = {
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
    }

    # Get response from the agent
    response = agent.invoke(state)
    messages = response.get("messages", [])

    # Extract last AI message
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    final_output = ai_messages[-1] if ai_messages else "No response received from the agent."

    # Return JSON-safe response
    return {
        "model": llm_id,
        "provider": provider,
        "response": final_output
    }
