from typing import Dict, Any, List


def initialize_state(input_data: Dict[str, Any]) -> Dict[str, Any]:
    return {

        # INPUT
        "farm_data": {
            "crop": input_data.get("crop"),
            "soil_type": input_data.get("soil_type"),
            "pH": input_data.get("pH"),
            "rainfall": input_data.get("rainfall"),
            "temperature": input_data.get("temperature"),
            "fertilizer": input_data.get("fertilizer"),
        },

        "user_query": input_data.get("query", ""),

        # ML OUTPUT
        "predicted_yield": None,      # float
        "yield_risk": None,           # LOW / MEDIUM / HIGH

        # CONTEXT AGENTS
        "soil_analysis": "",
        "weather_analysis": "",
        "crop_analysis": "",

        # combined analysis
        "final_analysis": "",

        # critic evaluation
        "analysis_score": 0,
        "analysis_feedback": "",

        # retry control
        "retry_count": 0,
        "max_retries": 2,

        # QUERY UNDERSTANDING
        "intent": "",

        # RAG
        "retrieved_docs": [],        # List[str]
        "retrieved_sources": [],     # List[str]

        # PLANNING
        "plan": "",

        # ADVICE AGENTS
        "fertilizer_advice": "",
        "irrigation_advice": "",
        "risk_advice": "",

        # final combined advice
        "final_advice": "",

        # SOURCES
        "sources": [],

        # FINAL OUTPUT
        "final_output": {
            "Status": "",
            "Advice": "",
            "Sources": [],
            "Disclaimer": ""
        }
    }