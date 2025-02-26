from langgraph.graph import StateGraph, START, END
from src.agents import retrieve_internal, fetch_air_quality, visualize_data
from typing import TypedDict
from langchain.schema import Document


# Define GraphState type for workflow transitions
class GraphState(TypedDict):
    question: str
    documents: list[Document]


def route_question(state: GraphState, llm):
    """Determine the appropriate agent based on the question."""
    question = state["question"]
    prompt = (
        f"Question: {question}\n"
        "Choose the most appropriate agent for this question. "
        "Return only one of the following exact options:\n"
        "- retrieve_internal\n"
        "- fetch_air_quality\n"
        "- visualize_data\n"
        "Do not provide any explanation, just return the exact name of the option."
    )
    response = llm.invoke(prompt)
    if hasattr(response, "content"):
        agent = response.content.strip()
    elif isinstance(response, str):
        agent = response.strip()
    else:
        raise ValueError("Unexpected response format from LLM.")
    agent = agent.replace("\\_", "_")
    valid_agents = {"retrieve_internal", "fetch_air_quality", "visualize_data"}
    if agent not in valid_agents:
        raise ValueError(f"Invalid agent selected by LLM: {agent}")
    return agent


def build_workflow(retriever, llm, air_quality_api):
    """Build and compile the state graph workflow."""
    workflow = StateGraph(GraphState)
    # Register agent nodes
    workflow.add_node(
        "retrieve_internal", lambda state: retrieve_internal(state, retriever, llm)
    )
    workflow.add_node(
        "fetch_air_quality",
        lambda state: fetch_air_quality(state, llm, air_quality_api),
    )
    workflow.add_node("visualize_data", visualize_data)
    # Add a conditional edge at the start to select the appropriate agent
    workflow.add_conditional_edges(
        START,
        lambda state: route_question(state, llm),
        {
            "retrieve_internal": "retrieve_internal",
            "fetch_air_quality": "fetch_air_quality",
            "visualize_data": "visualize_data",
        },
    )
    # Link each agent node to the end of the workflow
    workflow.add_edge("retrieve_internal", END)
    workflow.add_edge("fetch_air_quality", END)
    workflow.add_edge("visualize_data", END)
    return workflow.compile()
