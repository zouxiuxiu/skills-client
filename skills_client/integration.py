from typing import List, Callable
from .registry import SkillToolRegistry

# 如果你使用 LangChain
try:
    from langchain_core.tools import StructuredTool
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

def build_langchain_tools(registry: SkillToolRegistry, tool_names: List[str]) -> List:
    """将 registry 中的指定工具转换为 LangChain StructuredTool 列表"""
    if not HAS_LANGCHAIN:
        raise ImportError("langchain-core not installed")
    tools = []
    for name in tool_names:
        func = registry.get_tool(name)
        if func:
            tool = StructuredTool.from_function(
                name=name,
                func=func,
                description=registry.get_description(name) or f"Tool {name}"
            )
            tools.append(tool)
    return tools

def merge_skill_into_system_prompt(skill_instructions: str, base_prompt: str) -> str:
    if not skill_instructions:
        return base_prompt
    return f"{skill_instructions}\n\n【重要】严格按照上述步骤执行，并遵守 ReAct 格式。\n\n{base_prompt}"