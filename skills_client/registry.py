from typing import Callable, Dict, Optional, List
from .models import SkillMetadata

class SkillToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._descriptions: Dict[str, str] = {}

    def register_tool(self, name: str, func: Callable, description: Optional[str] = None):
        self._tools[name] = func
        if description:
            self._descriptions[name] = description

    def get_tool(self, name: str) -> Optional[Callable]:
        return self._tools.get(name)

    def get_description(self, name: str) -> str:
        return self._descriptions.get(name, "")

    def register_from_skill_metadata(self, skill_meta: SkillMetadata):
        """根据技能声明的 allowed_tools 自动注册（假设已经注册好）"""
        for tool_name in skill_meta.allowed_tools:
            if tool_name not in self._tools:
                print(f"Warning: tool '{tool_name}' not registered")

    def get_required_tools(self, skill_meta: SkillMetadata) -> List[Callable]:
        """返回技能所需工具的实际可调用对象列表"""
        tools = []
        for name in skill_meta.allowed_tools:
            func = self._tools.get(name)
            if func:
                tools.append(func)
            else:
                print(f"Warning: required tool '{name}' is not registered")
        return tools