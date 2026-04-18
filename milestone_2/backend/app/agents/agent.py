import logging
from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END

# ================= LOGGER =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= IMPORT NODES =================
from app.agents.nodes.ml_node import ml_node
from app.agents.nodes.risk_node import risk_node

from app.agents.nodes.context.soil_agent import soil_agent
from app.agents.nodes.context.weather_agent import weather_agent
from app.agents.nodes.context.crop_agent import crop_agent
from app.agents.nodes.context.critic_node import critic_node

from app.agents.nodes.rag_node import rag_node
from app.agents.nodes.planning_node import planning_node

from app.agents.nodes.advice.fertilizer_agent import fertilizer_agent
from app.agents.nodes.advice.irrigation_agent import irrigation_agent
from app.agents.nodes.advice.risk_agent import risk_agent
from app.agents.nodes.advice.synthesis import synthesis_node

from app.agents.nodes.source_node import source_node
from app.agents.nodes.output_node import output_node


# ================= STATE =================
class AgentState(TypedDict, total=False):
    farm_data: dict
    user_query: str

    predicted_yield: float
    yield_risk: str
    risk_reason: str

    soil_analysis: str
    weather_analysis: str
    crop_analysis: str

    analysis_score: int
    retry_count: int

    intent: str
    retrieved_docs: list
    retrieved_sources: list

    plan: str

    fertilizer_advice: str
    irrigation_advice: str
    risk_advice: str

    final_advice: str
    sources: list
    final_output: dict


# ================= INITIAL STATE =================
def initialize_state(input_data: dict) -> AgentState:
    farm_data = {}

    for k, v in input_data.items():
        if k != "query":
            farm_data[k] = v

    return {
        "farm_data": farm_data,
        "user_query": input_data.get("query", ""),
        "retry_count": 0
    }


# ================= BASIC NODES =================
def create_safe_wrapper(node_func):
    """
    Wraps existing node functions to reliably play nicely with LangGraph parallelism.
    Only returns new or modified keys to prevent overwriting the full TypedDict state.
    """
    def wrapper(state: AgentState):
        state_copy = state.copy()
        result_state = node_func(state_copy)
        
        diff = {}
        for k, v in result_state.items():
            if k not in state or state[k] != v:
                diff[k] = v
        return diff
    wrapper.__name__ = getattr(node_func, '__name__', 'wrapper')
    return wrapper

def input_node(state: AgentState) -> dict:
    return {"retry_count": 0}


def query_understanding_node(state: AgentState) -> dict:
    query = state.get("user_query", "").lower()

    if "fertilizer" in query:
        intent = "fertilizer"
    elif "water" in query or "irrigation" in query:
        intent = "irrigation"
    else:
        intent = "general"

    return {"intent": intent}


# ================= CRITIC WRAPPER =================
def wrapped_critic_node(state: AgentState) -> dict:
    score = critic_node(state)
    retry_count = state.get("retry_count", 0) + 1

    return {
        "analysis_score": score,
        "retry_count": retry_count
    }


def critic_condition(state: AgentState) -> str:
    score = state.get("analysis_score", 0)
    retry_count = state.get("retry_count", 0)

    logger.info(f"Critic Score: {score}, Retry: {retry_count}")

    if score < 7 and retry_count <= 2:
        return "loop"

    return "pass"


# ================= GRAPH =================
builder = StateGraph(AgentState)

# Nodes
builder.add_node("input", input_node)
builder.add_node("ml", create_safe_wrapper(ml_node))
builder.add_node("risk", create_safe_wrapper(risk_node))

# ✅ ADD THIS (context hub)
builder.add_node("context_start", lambda state: {})

builder.add_node("soil", create_safe_wrapper(soil_agent))
builder.add_node("weather", create_safe_wrapper(weather_agent))
builder.add_node("crop", create_safe_wrapper(crop_agent))
builder.add_node("critic", wrapped_critic_node)

builder.add_node("query", query_understanding_node)
builder.add_node("rag", create_safe_wrapper(rag_node))
builder.add_node("plan", create_safe_wrapper(planning_node))

builder.add_node("fertilizer", create_safe_wrapper(fertilizer_agent))
builder.add_node("irrigation", create_safe_wrapper(irrigation_agent))
builder.add_node("risk_advice", create_safe_wrapper(risk_agent))

builder.add_node("synthesis", create_safe_wrapper(synthesis_node))
builder.add_node("source", create_safe_wrapper(source_node))
builder.add_node("output", create_safe_wrapper(output_node))

# ================= EDGES =================
builder.add_edge(START, "input")
builder.add_edge("input", "ml")
builder.add_edge("ml", "risk")

# ✅ FIXED: use context_start instead of direct fan-out
builder.add_edge("risk", "context_start")

builder.add_edge("context_start", "soil")
builder.add_edge("context_start", "weather")
builder.add_edge("context_start", "crop")

builder.add_edge("soil", "critic")
builder.add_edge("weather", "critic")
builder.add_edge("crop", "critic")

# ✅ FIXED LOOP (important)
builder.add_conditional_edges(
    "critic",
    critic_condition,
    {
        "loop": "context_start",   # 🔥 FIXED
        "pass": "query"
    }
)

# RAG + Planning
builder.add_edge("query", "rag")
builder.add_edge("rag", "plan")

# Advice agents
builder.add_edge("plan", "fertilizer")
builder.add_edge("plan", "irrigation")
builder.add_edge("plan", "risk_advice")

builder.add_edge("fertilizer", "synthesis")
builder.add_edge("irrigation", "synthesis")
builder.add_edge("risk_advice", "synthesis")

# Final steps
builder.add_edge("synthesis", "source")
builder.add_edge("source", "output")
builder.add_edge("output", END)

# Compile graph
graph = builder.compile()


# ================= RUN FUNCTION =================
def run_agent(input_data: dict) -> dict:
    try:
        logger.info("Starting Agent Pipeline")

        state = initialize_state(input_data)
        final_state = graph.invoke(state)

        logger.info("Pipeline Completed")

        return final_state.get("final_output", final_state)

    except Exception as e:
        logger.exception("Error in run_agent")
        return {"error": str(e)}