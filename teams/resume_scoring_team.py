import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.parse_documents import *
from agents.resume_processing_agent import extract_resume_to_json
from agents.resume_summary_agent import get_resume_summary
from agents.resume_scoring_agent import resume_scoring_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_core.memory import MemoryContent, MemoryMimeType
from memory.memory_store import memory_model
from autogen_agentchat.messages import TextMessage


# def safe_json_parse(content):
#     if isinstance(content, dict):
#         return content
#     if isinstance(content, str):
#         try:
#             return json.loads(content)
#         except Exception:
#             try:
#                 return json.loads(content.replace("'", "\""))  # fallback
#             except Exception:
#                 return {"raw": content}
#     return {"raw": str(content)}

# ---- Main pipeline ----
def run_resume_team():
    try:
        team = RoundRobinGroupChat(
            participants=[
                extract_resume_to_json(),
                get_resume_summary(),
                resume_scoring_agent(),
            ],
            name="resume_scoring_team",
            description="Score resume from resume JSON text",
            termination_condition=MaxMessageTermination(4),
        )

        # resume_summary_json, resume_summary_str, resume_json, final_response_json = {}, "", {}, {}

        # async for response in team.run_stream(task=resume_text):
        #     if isinstance(response, TextMessage):
        #         if response.source.startswith("get_resume_summary"):
        #             resume_summary_json = safe_json_parse(response.content)
        #             resume_summary_str = json.dumps(resume_summary_json, sort_keys=True)
                
        #         elif response.source.startswith("extract_resume_to_json"):
        #             resume_json = safe_json_parse(response.content)

        #         elif response.source.startswith("resume_scoring_agent"):
        #             final_response_json = safe_json_parse(response.content)


        # # Save both summary & scoring in memory
        # chroma_user_memory = memory_model()
        # memory_bundle = {
        #     "summary": resume_summary_json,
        #     "scoring": final_response_json,
        # }

        # await chroma_user_memory.add(
        #     MemoryContent(
        #         content=json.dumps(memory_bundle),
        #         mime_type=MemoryMimeType.TEXT,
        #         metadata={"score": final_response_json.get("score", 0)},
        #     )
        # )

        # output = {
        #     "resume": resume_json,
        #     "resume_summary": resume_summary_str,
        #     "score": final_response_json
        # }
        # return output
        return team

    except Exception as e:
        print(f"Error while running the team: {e}")
        
