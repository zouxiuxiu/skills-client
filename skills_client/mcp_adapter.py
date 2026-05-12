import asyncio
from contextlib import asynccontextmanager
from .registry import SkillToolRegistry

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

class MCPToolAdapter:
    def __init__(self, registry: SkillToolRegistry):
        self.registry = registry

    @asynccontextmanager
    async def connect(self, command: str, args: list = None, env: dict = None):
        if not HAS_MCP:
            raise ImportError("mcp package not installed")
        server_params = StdioServerParameters(
            command=command,
            args=args or [],
            env=env,
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                for tool in tools.tools:
                    async def make_call(tool_name):
                        async def call(**kwargs):
                            result = await session.call_tool(tool_name, arguments=kwargs)
                            parts = []
                            for c in result.content:
                                if hasattr(c, 'text'):
                                    parts.append(c.text)
                            return "\n".join(parts)
                        return call
                    self.registry.register_tool(
                        name=tool.name,
                        func=make_call(tool.name),
                        description=tool.description
                    )
                yield