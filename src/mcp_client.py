"""Perseus MCP client — JSON-RPC 2.0 transport over HTTP.

Connects to the Perseus MCP server and provides a clean Python API
for each Perseus context tool used by the Slack agent.
"""

import json
import os
import httpx

from typing import Any


MCP_VERSION = "2025-06-18"
MCP_JSONRPC = "2.0"


class PerseusMCPClient:
    """Thin MCP client for Perseus tools over HTTP transport."""

    def __init__(self, base_url: str | None = None, timeout: float = 30.0):
        self.base_url = base_url or os.getenv("PERSEUS_MCP_URL", "http://localhost:5000/mcp")
        self.timeout = timeout
        self._request_id = 0

    # ── JSON-RPC helpers ──────────────────────────────────────────────────

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def _call_tool(self, tool_name: str, arguments: dict | None = None) -> dict[str, Any]:
        """Make a single JSON-RPC tools/call request."""
        payload = {
            "jsonrpc": MCP_JSONRPC,
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {},
            },
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(self.base_url, json=payload)
            resp.raise_for_status()
            data = resp.json()

        if "error" in data:
            raise RuntimeError(f"MCP error: {data['error']}")

        # Unwrap: result.content[0].text is the JSON-RPC answer
        result = data.get("result", {})
        content = result.get("content", [])
        if content and isinstance(content[0], dict):
            text = content[0].get("text", "")
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"text": text}
        return result

    async def list_tools(self) -> list[dict]:
        """Discover available Perseus tools."""
        payload = {
            "jsonrpc": MCP_JSONRPC,
            "id": self._next_id(),
            "method": "tools/list",
            "params": {},
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(self.base_url, json=payload)
            resp.raise_for_status()
            data = resp.json()
        return data.get("result", {}).get("tools", [])

    # ── Perseus tool methods ──────────────────────────────────────────────

    async def health(self) -> dict:
        """Check overall system health (services, skills, memory)."""
        return await self._call_tool("perseus_get_health")

    async def services(self) -> dict:
        """Get service health status."""
        return await self._call_tool("perseus_services")

    async def memory(self, query: str, k: int = 5) -> dict:
        """Recall memories via Mimir persistent memory."""
        return await self._call_tool("perseus_memory", {
            "query": query,
            "k": str(k),
            "mode": "search",
        })

    async def mimir(self, query: str, k: int = 5) -> dict:
        """Direct Mimir FTS5 recall."""
        return await self._call_tool("perseus_mimir", {
            "query": query,
            "k": str(k),
        })

    async def read(self, path: str, key: str | None = None) -> dict:
        """Read a file via Perseus @read."""
        args = {"path": path}
        if key:
            args["key"] = key
        return await self._call_tool("perseus_read", args)

    async def search(self, pattern: str, path: str = ".") -> dict:
        """Search files by glob or content pattern."""
        return await self._call_tool("perseus_search", {
            "pattern": pattern,
            "path": path,
        })

    async def list_dir(self, path: str = ".", limit: int = 20) -> dict:
        """List directory contents."""
        return await self._call_tool("perseus_list", {
            "path": path,
            "limit": str(limit),
        })

    async def tree(self, path: str = ".", depth: int = 2) -> dict:
        """Show directory tree."""
        return await self._call_tool("perseus_tree", {
            "path": path,
            "depth": str(depth),
        })

    async def skills(self, category: str | None = None, limit: int = 20) -> dict:
        """List available skills."""
        args = {"limit": str(limit)}
        if category:
            args["category"] = category
        return await self._call_tool("perseus_skills", args)

    async def date(self) -> dict:
        """Current date/time from the server."""
        return await self._call_tool("perseus_date")

    async def context(self) -> dict:
        """Get full workspace context."""
        return await self._call_tool("perseus_get_context")

    async def inbox(self, unread: bool = False, limit: int = 10) -> dict:
        """Check inbox messages."""
        return await self._call_tool("perseus_inbox", {
            "unread": "true" if unread else "false",
            "limit": str(limit),
        })

    async def session(self, count: int = 3) -> dict:
        """Recent session history."""
        return await self._call_tool("perseus_session", {
            "count": str(count),
        })
