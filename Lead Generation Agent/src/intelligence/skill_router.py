# src/intelligence/skill_router.py
import os
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

# Registry mapping workflow phase to skill prompt files
SKILLS_MAP = {
    "RESEARCH": ".agents/skills/geo-content/SKILL.md",
    "OUTBOUND": ".agents/skills/geo-citability/SKILL.md",
    "PROPOSAL": ".agents/skills/geo-proposal/SKILL.md",
    "AUDIT": ".agents/skills/geo-audit/SKILL.md",
    "SCHEMA": ".agents/skills/geo-schema/SKILL.md"
}

def resolve_skill_by_intent(intent_keyword: str) -> str:
    """
    Skill Router logic: Matches user/workflow intent to appropriate specialized skill.
    """
    key = intent_keyword.upper().strip()
    if "RESEARCH" in key or "CONTENT" in key:
        return SKILLS_MAP["RESEARCH"]
    elif "PROPOSAL" in key or "QUOTE" in key:
        return SKILLS_MAP["PROPOSAL"]
    elif "SCHEMA" in key or "JSON-LD" in key:
        return SKILLS_MAP["SCHEMA"]
    elif "AUDIT" in key or "GEO" in key:
        return SKILLS_MAP["AUDIT"]
    return SKILLS_MAP["OUTBOUND"]

def get_skill_instruction(phase_or_intent: str, workspace_root: Optional[str] = None) -> Dict[str, str]:
    """
    Dynamically loads the instruction package for a required skill without
    bloating the LLM context with unneeded skills.
    """
    relative_path = resolve_skill_by_intent(phase_or_intent)
    
    if workspace_root:
        full_path = os.path.join(workspace_root, relative_path)
    else:
        full_path = relative_path

    content = ""
    if os.path.exists(full_path):
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Could not read skill file at {full_path}: {e}")
            content = f"Instruction placeholder for skill {phase_or_intent}"
    else:
        content = f"Instruction placeholder for skill {phase_or_intent}"

    return {
        "intent": phase_or_intent,
        "skill_path": relative_path,
        "instructions": content
    }
