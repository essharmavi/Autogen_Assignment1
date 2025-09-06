import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.jd_processing_agent import extract_jd_to_json
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMessageTermination


async def run_jd_processing_team(resume_text):
    try:
        termination_condition = TextMessageTermination("extract_jd_to_json")
        team = RoundRobinGroupChat(
            participants=[
                
            ],
            name="run_jd_processing_team",
            description="Get json text from job description",
            termination_condition=termination_condition
        )

        resume_summary_json, resume_summary_str, resume_json, final_response_json = {}, "", {}, {}

        async for response in team.run_stream(task=resume_text):


        return output

    except Exception as e:
        print(f"Error while running the team: {e}")
        return {}
