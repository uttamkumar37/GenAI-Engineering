from __future__ import annotations

# written against the `mcp` python sdk's stdio client pattern (mcp>=1.0); verify against
# the current SDK release, the transport/session API has shifted across versions
import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "mcp_server_basic", "server.py"
)


async def drive_conversation() -> None:
    server_params = StdioServerParameters(command="python3", args=[SERVER_SCRIPT])

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Discovered tools:", [t.name for t in tools.tools])

            calc_result = await session.call_tool("calculator", {"expression": "6 * 7"})
            print("calculator(6 * 7) ->", calc_result.content)

            search_result = await session.call_tool(
                "document_search", {"query": "vector database embeddings"}
            )
            print("document_search(...) ->", search_result.content)

            resources = await session.list_resources()
            print("Discovered resources:", [r.uri for r in resources.resources])


if __name__ == "__main__":
    asyncio.run(drive_conversation())
