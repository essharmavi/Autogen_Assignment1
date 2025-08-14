import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from chat_model.chat_model import get_model_client
from prompts.prompts import prompts_dict


async def extract_jd_to_json(resume_text: str) -> dict:
    """Extract key data from resume text and return in JSON format."""
    model_client = get_model_client()
    agent = AssistantAgent(
        name="extract_jd_to_json",
        model_client=model_client,
        description="Extract key data from Job description(jd) text and convert to JSON format",
        system_message=prompts_dict["json_extract_jd_prompt"],
    )
    result = await agent.run(task=resume_text)
    last_message = result.messages[-1].content
    return last_message
