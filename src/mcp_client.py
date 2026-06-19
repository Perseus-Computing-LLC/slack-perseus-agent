"""Perseus MCP client — JSON-RPC 2.0 transport over HTTP.

Connects to the Perseus MCP server and provides a clean Python API
for each Perseus context tool used by the Slack agent.
"""

import json
import os
import re
import httpx

from typing import Any


MCP_VERSION = "2025-06-18"
MCP_JSONRPC = "2.0"

# Perseus has no server-side search tool, so `search()` enumerates files via
# perseus_list and greps their contents via perseus_read, client-side. These
# bounds keep a single search to a handful of round-trips.
SEARCHABLE_EXTENSIONS = (
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb",
    ".c", ".h", ".cpp", ".hpp", ".cs", ".php", ".swift", ".kt", ".scala",
    ".sh", ".bash", ".zsh", ".sql", ".md", ".txt", ".rst", ".toml",
    ".yaml", ".yml", ".json", ".ini", ".cfg", ".env", ".html", ".css",
)
SEARCH_MAX_FILES = 40        # cap files read per search
SEARCH_MAX_MATCHES = 60      # cap returned matches
SEARCH_MAX_DEPTH = 4         # directory recursion depth
SEARCH_MAX_LINE_LEN = 240    # truncate long matched lines


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

    # ── Response normalization ────────────────────────────────────────────

    @staticmethod
    def _result_text(data: Any) -> str:
        """Best-effort extract the textual payload from a tool result.

        Perseus filesystem tools render markdown, so `_call_tool` returns
        ``{"text": "..."}``; structured deployments may use ``content``.
        """
        if isinstance(data, str):
            return data
        if not isinstance(data, dict):
            return ""
        for key in ("content", "text", "rendered", "body", "output"):
            val = data.get(key)
            if isinstance(val, str) and val.strip():
                return val
        return ""

    @staticmethod
    def _is_error_text(text: str) -> bool:
        """Detect Perseus warning/not-found banners returned as content."""
        t = text.strip()
        if t.startswith(("> ⚠", "⚠", "> ❌", "❌")):
            return True
        return "not found" in t.lower() and "@" in t

    @staticmethod
    def _extract_entry_name(line: str) -> str:
        """Pull a single file/dir name out of one line of `perseus_list` output.

        Tolerant of bullets, blockquotes, and table rows; returns "" for
        headers, separators, and noise.
        """
        s = line.strip()
        if not s:
            return ""
        s = re.sub(r"^>\s?", "", s)          # blockquote marker
        s = re.sub(r"^[-*•]\s+", "", s)      # list bullet
        s = s.strip("|").strip()             # table cell padding
        if not s or s[0] in "#`─—=─":
            return ""
        m = re.match(r"([\w.][\w.\-]*/?)", s)
        if not m:
            return ""
        tok = m.group(1)
        if tok.lower() in ("name", "size", "type", "modified", "total", "dir", "file"):
            return ""
        return tok

    async def _list_names(self, path: str) -> tuple[list[str], list[str]]:
        """Return (dir_names, file_names) for a single directory, best-effort."""
        try:
            data = await self._call_tool("perseus_list", {"path": path, "limit": "200"})
        except Exception:
            return [], []
        text = self._result_text(data)
        dirs: list[str] = []
        files: list[str] = []
        if not text and isinstance(data, dict):
            entries = data.get("entries") or data.get("items") or []
            for e in entries:
                if not isinstance(e, dict):
                    continue
                name = e.get("name", "")
                if not name:
                    continue
                (dirs if e.get("type") == "dir" or name.endswith("/") else files).append(name.rstrip("/"))
            return dirs, files
        for line in text.splitlines():
            name = self._extract_entry_name(line)
            if not name:
                continue
            if name.endswith("/"):
                dirs.append(name.rstrip("/"))
            elif "." in name:
                files.append(name)
            else:
                dirs.append(name)  # ambiguous → try as dir; failed lists no-op
        return dirs, files

    async def _enumerate_files(self, root: str, max_files: int, max_depth: int) -> list[str]:
        """Recursively collect searchable file paths under ``root``."""
        found: list[str] = []

        async def walk(path: str, depth: int) -> None:
            if len(found) >= max_files or depth > max_depth:
                return
            dirs, files = await self._list_names(path)
            base = "" if path in ("", ".") else path.rstrip("/")
            for f in files:
                if f.lower().endswith(SEARCHABLE_EXTENSIONS):
                    found.append(f"{base}/{f}" if base else f)
                    if len(found) >= max_files:
                        return
            for d in dirs:
                if len(found) >= max_files:
                    return
                if d.startswith("."):          # skip .git, hidden dirs
                    continue
                await walk(f"{base}/{d}" if base else d, depth + 1)

        await walk(root or ".", 0)
        return found[:max_files]

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
        """Read a file via Perseus @read, normalized to {path, content, truncated}."""
        args = {"path": path}
        if key:
            args["key"] = key
        data = await self._call_tool("perseus_read", args)
        text = self._result_text(data)
        if not text or self._is_error_text(text):
            return {"path": path, "content": "", "truncated": False,
                    "error": (text or "not found").strip()}
        return {
            "path": path,
            "content": text,
            "truncated": bool(isinstance(data, dict) and data.get("truncated")),
        }

    async def search(self, pattern: str, path: str = ".") -> dict:
        """Content search across project files (client-side).

        Perseus exposes no server-side search tool, so this enumerates files
        with perseus_list and greps their contents with perseus_read, in
        Python. Bounded by SEARCH_MAX_* to keep round-trips and output sane.
        Returns {matches, count, files_scanned, files_found}; never raises.
        """
        needle = (pattern or "").strip()
        if not needle:
            return {"matches": [], "count": 0, "files_scanned": 0, "files_found": 0}

        files = await self._enumerate_files(path or ".", SEARCH_MAX_FILES, SEARCH_MAX_DEPTH)
        low = needle.lower()
        matches: list[dict] = []
        scanned = 0

        for fpath in files:
            if len(matches) >= SEARCH_MAX_MATCHES:
                break
            try:
                fdata = await self.read(fpath)
            except Exception:
                continue
            content = fdata.get("content", "")
            if not content:
                continue
            scanned += 1
            for i, line in enumerate(content.splitlines(), start=1):
                if low in line.lower():
                    snippet = line.strip()
                    if len(snippet) > SEARCH_MAX_LINE_LEN:
                        snippet = snippet[:SEARCH_MAX_LINE_LEN] + "…"
                    matches.append({"file": fpath, "line_number": i, "content": snippet})
                    if len(matches) >= SEARCH_MAX_MATCHES:
                        break

        return {
            "matches": matches,
            "count": len(matches),
            "files_scanned": scanned,
            "files_found": len(files),
        }

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
