import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from teams.resume_scoring_team import run_resume_team
from agents.jd_processing_agent import extract_jd_to_json
from agents.jd_compare_resume_agent import compare_jd_resume_agent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMessageTermination
from autogen_core.memory import MemoryContent, MemoryMimeType
from memory.memory_store import memory_model

# --- Helper: safe JSON parsing ---
def safe_json_parse(content):
    if isinstance(content, dict):
        return content
    if isinstance(content, str):
        try:
            return json.loads(content)
        except Exception:
            try:
                return json.loads(content.replace("'", "\""))  # fallback
            except Exception:
                return {"raw": content}
    return {"raw": str(content)}

async def run_final_team(resume_text, jd_text):
    try:

        team = RoundRobinGroupChat(
            participants=[
                run_resume_team(),
                extract_jd_to_json(),
                compare_jd_resume_agent()
            ],
            name="final_team",
            description="Process resume and JD, then compare them",
            termination_condition=TextMessageTermination("compare_jd_resume_agent")
        )

        task = [TextMessage(content=resume_text, source="user"), TextMessage(content=jd_text, source="user")]
        resume_summary_json, resume_summary_str, resume_json, final_response_json = {}, "", {}, {}
        async for response in team.run_stream(task=task):
            if isinstance(response, TextMessage):
                if response.source.startswith("get_resume_summary"):
                    resume_summary_json = safe_json_parse(response.content)
                    resume_summary_str = json.dumps(resume_summary_json, sort_keys=True)
                
                elif response.source.startswith("extract_resume_to_json"):
                    resume_json = safe_json_parse(response.content)

                elif response.source.startswith("resume_scoring_agent"):
                    final_response_json = safe_json_parse(response.content)
                elif response.source.startswith("extract_jd_to_json"):
                    jd_json = safe_json_parse(response.content)
                elif response.source.startswith("compare_jd_resume_agent"):
                    comparison_json = safe_json_parse(response.content)

        # Save both summary & scoring in memory
        chroma_user_memory = memory_model()
        memory_bundle = {
            "summary": resume_summary_json,
            "scoring": final_response_json,
        }

        await chroma_user_memory.add(
            MemoryContent(
                content=json.dumps(memory_bundle),
                mime_type=MemoryMimeType.TEXT,
                metadata={"score": final_response_json.get("score", 0)},
            )
        )

        output = {
            "resume": resume_json,
            "resume_summary": resume_summary_str,
            "score": final_response_json,
            "jd_json": jd_json,
            "comparison": comparison_json
        }
        return output
                    

    except Exception as e:
        print(f"Error while running the final team: {e}")
        return {}