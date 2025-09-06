import os
import sys
import asyncio
import hashlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from chat_model.chat_model import get_model_client
from prompts.prompts import prompts_dict
from memory.memory_store import memory_model


def resume_scoring_agent():
    
    model_client = get_model_client()
    agent = AssistantAgent(
        name="resume_scoring_agent",
        model_client=model_client,
        description="Evaluate a given resume and score it.",
        system_message=prompts_dict["resume_scoring"],
        memory= [memory_model()]
    )

    # result = await agent.run(task=resume_text)
    # last_message = result.messages[-1].content


    return agent