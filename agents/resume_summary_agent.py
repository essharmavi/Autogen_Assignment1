import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from chat_model.chat_model import get_model_client
from prompts.prompts import prompts_dict

def get_resume_summary():
    """Create a resume summary with kewords that will go into our vector store."""
    model_client = get_model_client()
    agent = AssistantAgent(
        name="get_resume_summary",
        model_client=model_client,
        description="Create a resume summary with kewords that will go into our vector store.",
        system_message=prompts_dict["resume_summary"],
    )
    # result = await agent.run(task=resume_text)
    # last_message = result.messages[-1].content
    return agent