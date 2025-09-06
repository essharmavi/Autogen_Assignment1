import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from chat_model.chat_model import get_model_client
from prompts.prompts import prompts_dict


def compare_jd_resume_agent() :
    """Compare resume and JD."""
    model_client = get_model_client()
    agent = AssistantAgent(
        name="compare_jd_resume_agent",
        model_client=model_client,
        description="Compare resume and JD",
        system_message=prompts_dict["compare_resume_jd"],
    )
    return agent