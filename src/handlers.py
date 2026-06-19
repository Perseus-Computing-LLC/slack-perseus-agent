"""Intent routing for Perseus Slack agent.

Parses user messages, determines intent, calls the appropriate
Perseus MCP tool, and returns formatted Slack blocks.
"""

import re

from src.mcp_client import PerseusMCPClient
from src import blocks


# ── Intent patterns ─────────────────────────────────────────────────────────

INTENT_PATTERNS = [
    # (regex, intent_name, group_for_query)
    (r"^(?:services?|health|status)$", "services", None),
    (r"^memory\s+(.+)$", "memory", 1),
    (r"^remember\s+(.+)$", "memory", 1),
    (r"^recall\s+(.+)$", "memory", 1),
    (r"^search\s+(.+)$", "search", 1),
    (r"^find\s+(.+)$", "search", 1),
    (r"^read\s+(.+)$", "read", 1),
    (r"^show\s+(.+)$", "read", 1),
    (r"^skills?$", "skills", None),
    (r"^tools?$", "skills", None),
    (r"^onboard(?:ing)?$", "onboard", None),
    (r"^help$", "help", None),
    (r"^context$", "context", None),
    (r"^inbox$", "inbox", None),
    (r"^date|time$", "date", None),
    (r"^ask\s+(.+)$", "ask", 1),
    (r"^(.+)$", "ask", 1),  # fallback — treat as natural language
]


def parse_intent(text: str) -> tuple[str, str | None]:
    """Parse a user message into (intent, query_or_path)."""
    text = text.strip()
    for pattern, intent, query_group in INTENT_PATTERNS:
        m = re.match(pattern, text, re.IGNORECASE)
        if m:
            query = m.group(query_group).strip() if query_group else None
            return intent, query
    return "ask", text


# ── Handler ─────────────────────────────────────────────────────────────────

class PerseusHandler:
    """Routes Slack messages to Perseus MCP tools."""

    def __init__(self, mcp_url: str | None = None):
        self.client = PerseusMCPClient(mcp_url)

    async def handle(self, text: str) -> list[dict]:
        """Process a user message and return Slack blocks."""
        intent, query = parse_intent(text)

        try:
            if intent == "services":
                data = await self.client.services()
                return blocks.services_blocks(data)

            elif intent == "memory":
                data = await self.client.memory(query or "recent decisions")
                return blocks.memory_blocks(data, query or "")

            elif intent == "search":
                data = await self.client.search(query or "*")
                return blocks.search_blocks(data, query or "")

            elif intent == "read":
                data = await self.client.read(query or "AGENTS.md")
                return blocks.read_blocks(data)

            elif intent == "skills":
                data = await self.client.skills()
                return blocks.services_blocks(data)  # reuse similar format

            elif intent == "onboard":
                # Gather multiple context sources
                try:
                    services_data = await self.client.services()
                except Exception:
                    services_data = {"services": []}
                try:
                    skills_data = await self.client.skills()
                except Exception:
                    skills_data = {"skills": []}
                try:
                    memory_data = await self.client.memory("decision", k=3)
                except Exception:
                    memory_data = {"results": []}
                return blocks.onboarding_blocks(skills_data, services_data, memory_data)

            elif intent == "help":
                return blocks.help_blocks()

            elif intent == "context":
                data = await self.client.context()
                return blocks.context_blocks(data)

            elif intent == "inbox":
                data = await self.client.inbox()
                return blocks.read_blocks(data)  # reuse read format

            elif intent == "date":
                data = await self.client.date()
                dt = data.get("datetime", data.get("iso8601", ""))
                return [{
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"🕐 Server time: `{dt}`"},
                }]

            elif intent == "ask":
                # Natural language: try memory first, fall back to context
                try:
                    data = await self.client.memory(query or "context", k=5)
                    return blocks.memory_blocks(data, query or "")
                except Exception:
                    data = await self.client.context()
                    return blocks.context_blocks(data)

            else:
                return blocks.help_blocks()

        except Exception as e:
            return blocks.error_blocks(str(e))
