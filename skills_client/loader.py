import re
import yaml
from pathlib import Path
from typing import List, Optional
from .models import Skill, SkillMetadata

def load_skill_from_dir(skill_dir: str) -> Optional[Skill]:
    skill_file = Path(skill_dir) / "SKILL.md"
    if not skill_file.exists():
        return None

    content = skill_file.read_text(encoding="utf-8")
    pattern = r'^---\n(.*?)\n---\n(.*)$'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid SKILL.md format in {skill_file}")

    frontmatter = yaml.safe_load(match.group(1))
    markdown_body = match.group(2).strip()

    metadata = SkillMetadata(
        name=frontmatter.get("name"),
        description=frontmatter.get("description"),
        version=frontmatter.get("version", "1.0.0"),
        author=frontmatter.get("author"),
        allowed_tools=frontmatter.get("allowed-tools", []),
    )
    return Skill(metadata=metadata, instructions=markdown_body)

def list_all_skills(skills_root: str = "skills") -> List[Skill]:
    skills = []
    root_path = Path(skills_root)
    if not root_path.exists():
        return skills
    for skill_dir in root_path.iterdir():
        if skill_dir.is_dir():
            skill = load_skill_from_dir(str(skill_dir))
            if skill:
                skills.append(skill)
    return skills