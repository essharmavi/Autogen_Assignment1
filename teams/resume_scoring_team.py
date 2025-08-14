import os
import sys
import json
import streamlit as st
import hashlib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.parse_documents import *
from agents.resume_processing_agent import extract_resume_to_json
from agents.jd_processing_agent import extract_jd_to_json
from agents.resume_scoring_agent import resume_scoring_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination

async def run_resume_team(resume_text):
    try:
        # hash_resume_text = hashlib.sha256(resume_text.encode("utf-8")).hexdigest()
        team = RoundRobinGroupChat(
            participants= [extract_resume_to_json(),resume_scoring_agent()],
            name= "run_resume_team",
            description = "Score resume from resume JSON text",
            # termination_condition= TextMentionTermination("Terminate"),
            termination_condition= MaxMessageTermination(3)
        )
        # - You are the last agent in the Team. So always end with Terminate as well along with JSOn output.
        result = await Console(team.run_stream(task=resume_text))
        



        resume_text_json  = json.loads(result.messages[-2].content)
        resume_text_str = json.dumps(resume_text_json, sort_keys=True)
        hash_resume_text = hashlib.sha256(resume_text_str.encode("utf-8")).hexdigest()
        final_response_json = json.loads(result.messages[-1].content)

        resume_score_dict = {
        hash_resume_text: final_response_json
    }
    #     memory_store(resume_score)
        return final_response_json, resume_score_dict
    except Exception as e:
        print(f"Error while running the team: {e}")
