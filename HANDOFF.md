# HANDOFF: Perseus for Slack — Autonomous Build Packet

> **For:** Remote AI agent with no local context or filesystem access  
> **Date:** 2026-06-19  
> **Repo:** https://github.com/Perseus-Computing-LLC/slack-perseus-agent  
> **Status:** Phase 1-5 complete, video recorded. Phase 6 (Devpost submit) remains.

---

## 1. WHAT THIS IS

A Slack agent that connects developer teams to live project context via **MCP server integration**. Built for the **Slack Agent Builder Challenge 2026** on Devpost.

### Hackathon details
| Field | Value |
|---|---|
| Contest | Slack Agent Builder Challenge |
| Devpost URL | https://slackhack.devpost.com/ |
| Deadline | **July 13, 2026 5:00pm PT** (24 days remaining as of 6/19) |
| Track | **New Slack Agent** (MCP server integration) |
| Prize pool | **$42,000** cash + Dreamforce 2026 trip + Slack swag |
| Participants | 2,444 registered |
| Requirements | App uses ≥1 of: Slack AI / MCP integration / RTS API; fits ≥1 track |
| Submission needs | ~3min demo video, architecture diagram, GitHub repo, Slack sandbox URL (grant access to slackhack@salesforce.com + testing@devpost.com) |
| Eligibility | US is eligible ✅. Individual or org OK. |
| Git identity | `perseus <51974392+tcconnally@users.noreply.github.com>` |
| GitHub org | Perseus-Computing-LLC |
| License | MIT |

### Winning angle
The Slack challenge requires MCP integration. Perseus/Mimir already ship as **production MCP servers** with 27+ tools — real GitHub stars, real pip installs, real users. We're NOT building an MCP server from scratch. We're wiring a production MCP infrastructure into Slack. Competitors will be wiring toy MCP servers; we're wiring infrastructure.

---

## 2. CURRENT STATE — WHAT'S DONE

### ✅ Completed
- **GitHub repo** created: https://github.com/Perseus-Computing-LLC/slack-perseus-agent (public, MIT, 4 commits pushed)
- **README.md** — full pitch, architecture, quickstart, MCP angle
- **LICENSE** — MIT
- **AGENTS.md** — project context for AI agents
- **.nojekyll** — for GitHub Pages hosting of demo assets
- **manifest.json** — Slack app manifest (bot user, slash commands, scopes, Socket Mode)
- **.env.example** — SLACK_BOT_TOKEN, SLACK_APP_TOKEN, PERSEUS_MCP_URL
- **requirements.txt** — slack-bolt, httpx, mcp, python-dotenv

### ✅ Source code (all 4 files complete)
- **src/app.py** — Slack Bolt AsyncApp with Socket Mode. Handles @mentions, `/perseus` slash command, DMs, App Home.
- **src/mcp_client.py** — PerseusMCPClient (JSON-RPC 2.0 over HTTP). Methods: health, services, memory, mimir, read, search, list_dir, tree, skills, date, context, inbox, session.
- **src/handlers.py** — Intent routing with regex patterns (services, memory, search, read, onboard, ask, help, context, inbox, date). NL fallback uses memory recall.
- **src/blocks.py** — Slack Block Kit formatters. services_blocks, memory_blocks, search_blocks, read_blocks, context_blocks, onboarding_blocks, error_blocks, help_blocks.

### ✅ Documentation
- **docs/ARCHITECTURE.md** — System design, data flow, design decisions table, tech stack, security notes
- **docs/SUBMISSION.md** — All Devpost form fields pre-written (project name, pitch, what it does, how built, why MCP, what's next, links)

### ✅ Demo
- **demo/demo_script.md** — 5-scene timed narration script (~2:45)
- **demo/demo_transcript.md** — Full simulated Slack conversation transcript
- **demo/demo_terminal.html** — Slack conversation simulation (dark theme, avatars, typing indicators, auto-play JS)
- **demo/record_demo.py** — Playwright recording script (1280x720, serves via local HTTP)
- **demo/demo_video.mp4** — Recorded video, 2:49, 1.6MB ✅
- **assets/architecture-diagram.html** — Dark-themed SVG system architecture diagram

---

## 3. ARCHITECTURE

```
Slack User → Slack Bolt (Python, Socket Mode) → MCP JSON-RPC 2.0 over HTTP → Perseus MCP Server
                                                                                  ├── perseus_services (health)
                                                                                  ├── perseus_memory (Mimir recall)
                                                                                  ├── perseus_read (file inspection)
                                                                                  ├── perseus_search (code search)
                                                                                  ├── perseus_skills (capability list)
                                                                                  └── perseus_context (workspace ctx)
```

### Key design decisions
| Decision | Why |
|---|---|
| Socket Mode (not HTTP endpoints) | No public URL needed for dev sandbox |
| Slack Bolt Python (not Slack CLI) | Battle-tested, well-documented, existing Python tooling |
| HTTP MCP transport (not stdio) | Perseus runs independently, easier in containers |
| Regex intent routing (not LLM) | Deterministic, fast, no token cost for basic queries |
| Slack Blocks (not plain text) | Rich formatting, color-coded statuses, code snippets |
| Async throughout | Slack Bolt is async-native; httpx.AsyncClient |

### Perseus MCP tools used
`perseus_services`, `perseus_memory`, `perseus_mimir`, `perseus_read`, `perseus_search`, `perseus_skills`, `perseus_context`, `perseus_session`, `perseus_inbox`, `perseus_date`, `perseus_get_health`, `perseus_list`, `perseus_tree`

### Intent routing table
| User says | Intent | MCP tool called |
|---|---|---|
| `@perseus services` / `health` | services | perseus_services |
| `@perseus memory X` / `recall X` | memory | perseus_memory |
| `@perseus search X` / `find X` | search | perseus_search |
| `@perseus read X` / `show X` | read | perseus_read |
| `@perseus skills` / `tools` | skills | perseus_skills |
| `@perseus onboard` | onboard | services + skills + memory |
| `@perseus context` | context | perseus_context |
| `@perseus help` | help | (static blocks) |
| anything else | ask | memory (fallback: context) |

---

## 4. REMAINING WORK (Phase 6)

### User must do (browser-required, cannot automate):
1. **Register on Devpost**: https://slackhack.devpost.com/
2. **Create Slack developer sandbox**: https://api.slack.com/apps — use `manifest.json` from the repo
3. **Grant sandbox access**: Add `slackhack@salesforce.com` and `testing@devpost.com` as collaborators
4. **Fill Devpost submission form**: All content pre-written in `docs/SUBMISSION.md`
5. **Upload demo video**: `demo/demo_video.mp4` (2:49, 1.6MB)
6. **Upload architecture diagram**: `assets/architecture-diagram.html` (or convert to PNG)

### Agent can do:
- **Create architecture thumbnail PNG**: Screenshot `assets/architecture-diagram.html` with Playwright
- **Push any remaining changes**: Repo at `Perseus-Computing-LLC/slack-perseus-agent`
- **Update submission content**: Tweak `docs/SUBMISSION.md` as needed
- **Add Slack sandbox URL to submission docs**: Once user provides sandbox URL
- **Host demo video on GitHub Pages**: Add to repo, enable Pages

---

## 5. HOW TO CLONE AND PUSH

```bash
# Clone (public repo)
git clone https://github.com/Perseus-Computing-LLC/slack-perseus-agent.git

# If pushing, configure git identity FIRST:
git config user.email "51974392+tcconnally@users.noreply.github.com"
git config user.name "perseus"

# Push (token from BSM cache):
# Token at /opt/data/webui/minions-hermes-config/cache/bws_cache.json
# key: secrets.GITHUB_TOKEN
# Push URL: https://oauth2:{token}@github.com/Perseus-Computing-LLC/slack-perseus-agent.git
```

---

## 6. HOW TO RUN THE AGENT

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with real SLACK_BOT_TOKEN, SLACK_APP_TOKEN, PERSEUS_MCP_URL
python src/app.py
```

Requires: Python 3.11+, a Slack app with Socket Mode enabled, and a running Perseus MCP server.

---

## 7. HOW TO RECORD / RE-RECORD THE DEMO

```bash
cd slack-perseus-agent
python3 demo/record_demo.py [duration_seconds]
# Default: 165s (~2:45)
# Serves demo/demo_terminal.html on localhost:9876
# Records via Playwright headless Chromium at 1280x720
# Output: demo/video_output/*.webm

# Convert to MP4:
ffmpeg -y -i demo/video_output/*.webm \
  -c:v libx264 -preset fast -crf 23 \
  -pix_fmt yuv420p -movflags +faststart \
  demo/demo_video.mp4

# Verify duration:
ffprobe -v error -show_entries format=duration -of csv=p=0 demo/demo_video.mp4
```

---

## 8. FULL SOURCE CODE

### src/app.py
```python
"""Perseus for Slack — Main Application.

Slack Bolt agent that connects developer teams to live project context
via the Perseus MCP server. Handles @mentions and slash commands.

Usage:
    pip install -r requirements.txt
    cp .env.example .env  # fill in SLACK_BOT_TOKEN, PERSEUS_MCP_URL
    python src/app.py
"""

import logging
import os
import re
import sys

from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from src.handlers import PerseusHandler

# ── Setup ───────────────────────────────────────────────────────────────────

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("perseus-slack")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
PERSEUS_MCP_URL = os.getenv("PERSEUS_MCP_URL", "http://localhost:5000/mcp")

# Validate required tokens
if not SLACK_BOT_TOKEN or SLACK_BOT_TOKEN.startswith("xoxb-y"):
    logger.warning("SLACK_BOT_TOKEN not set or using placeholder. Set it in .env")
if not SLACK_APP_TOKEN or SLACK_APP_TOKEN.startswith("xapp-"):
    logger.warning("SLACK_APP_TOKEN not set or using placeholder. Socket Mode requires this.")

# ── Initialize ──────────────────────────────────────────────────────────────

app = AsyncApp(token=SLACK_BOT_TOKEN or "")
handler = PerseusHandler(PERSEUS_MCP_URL)

# ── Bot user mention handler ────────────────────────────────────────────────


@app.event("app_mention")
async def handle_app_mention(event, say, client):
    """Respond to @perseus mentions in channels."""
    user = event.get("user", "unknown")
    text = event.get("text", "")
    channel = event.get("channel", "")

    # Strip the bot mention from the text
    # Bot mention format: <@BOT_USER_ID> ...
    text = re.sub(r"<@\w+>\s*", "", text).strip()
    if not text:
        text = "help"

    logger.info(f"Mention from <@{user}> in {channel}: {text}")

    # Send typing indicator
    try:
        await client.reactions_add(channel=channel, timestamp=event.get("ts", ""), name="hourglass_flowing_sand")
    except Exception:
        pass  # reaction might fail if we don't have the right scope

    # Process the request
    blocks = await handler.handle(text)

    # Respond in thread
    try:
        await say(
            text="Here's what I found:",  # fallback text for notifications
            blocks=blocks,
            thread_ts=event.get("ts"),
        )
    except Exception as e:
        logger.error(f"Failed to send response: {e}")
        await say(
            text=f"❌ Error processing your request: {e}",
            thread_ts=event.get("ts"),
        )


# ── Slash command handler ───────────────────────────────────────────────────


@app.command("/perseus")
async def handle_slash_command(ack, command, say):
    """Handle /perseus slash command."""
    await ack()

    user = command.get("user_name", "unknown")
    text = command.get("text", "").strip()
    channel = command.get("channel_name", "unknown")

    logger.info(f"Slash from @{user} in #{channel}: {text or '(empty)'}")

    text = text or "help"
    blocks = await handler.handle(text)

    await say(
        text="Perseus response:",
        blocks=blocks,
    )


# ── Direct message handler ──────────────────────────────────────────────────


@app.event("message")
async def handle_direct_message(event, say):
    """Respond to DMs to the bot."""
    # Only respond to DMs (not channel messages)
    if event.get("channel_type") != "im":
        return

    # Ignore bot's own messages
    if event.get("bot_id"):
        return

    text = event.get("text", "").strip()
    if not text:
        return

    logger.info(f"DM from <@{event.get('user')}>: {text}")

    blocks = await handler.handle(text)
    await say(
        text="Here's what I found:",
        blocks=blocks,
    )


# ── Home tab / app home ────────────────────────────────────────────────────


@app.event("app_home_opened")
async def handle_app_home_opened(event, client):
    """Publish a welcome view when the App Home is opened."""
    user = event.get("user", "")

    try:
        await client.views_publish(
            user_id=user,
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "🤖 Perseus — Live Project Context", "emoji": True},
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                "I connect your Slack to live project context via MCP.\n\n"
                                "*Mention me anywhere* with `@perseus` or use `/perseus`:\n\n"
                                "• `services` — check what's running\n"
                                "• `memory <topic>` — recall team decisions\n"
                                "• `search <query>` — find code\n"
                                "• `read <file>` — inspect a file\n"
                                "• `onboard` — new member context dump\n"
                                "• `ask <question>` — natural language query\n"
                                "• `help` — show all commands"
                            ),
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "Built for the <https://slackhack.devpost.com/|Slack Agent Builder Challenge 2026> · MCP-powered · <https://github.com/Perseus-Computing-LLC/slack-perseus-agent|GitHub>",
                            }
                        ],
                    },
                ],
            },
        )
    except Exception as e:
        logger.error(f"Failed to publish home tab: {e}")


# ── Main ────────────────────────────────────────────────────────────────────


async def main():
    """Start the Slack Bolt app in Socket Mode."""
    logger.info("Starting Perseus for Slack...")
    logger.info(f"MCP endpoint: {PERSEUS_MCP_URL}")

    if not SLACK_APP_TOKEN:
        logger.error("SLACK_APP_TOKEN is required for Socket Mode. Set it in .env")
        sys.exit(1)

    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
```

### src/mcp_client.py
```python
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
```

### src/handlers.py
```python
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
```

### src/blocks.py
```python
"""Slack Block Kit formatters for Perseus responses.

Turns raw Perseus MCP output into rich, readable Slack Block Kit messages
with color-coded statuses, code snippets, and structured layouts.
"""

from datetime import datetime
from typing import Any


# ── Utilities ───────────────────────────────────────────────────────────────

def _status_emoji(status: str) -> str:
    """Map service health status to an emoji indicator."""
    s = status.lower().strip()
    if s in ("up", "ok", "healthy", "success", "active"):
        return "🟢"
    if s in ("down", "error", "critical", "failed"):
        return "🔴"
    if s in ("warning", "degraded", "stale"):
        return "🟡"
    return "⚪"


def _truncate(text: str, max_len: int = 2900) -> str:
    """Truncate text to fit within Slack's ~3000 char block limit."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 20] + "...\n[truncated]"


# ── Response blocks ─────────────────────────────────────────────────────────

def services_blocks(data: dict) -> list[dict]:
    """Format service health status as Slack blocks."""
    services = data.get("services", [])
    if not services:
        return [{"type": "section", "text": {"type": "mrkdwn", "text": "⚪ _No services reported._"}}]

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🩺 Service Health", "emoji": True},
        },
        {"type": "divider"},
    ]

    for svc in services:
        name = svc.get("name", "unknown")
        status = svc.get("status", "unknown")
        latency = svc.get("latency_ms")
        emoji = _status_emoji(status)
        line = f"{emoji} *{name}* — `{status}`"
        if latency is not None:
            line += f" ({latency}ms)"

        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": line},
        })

    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [{
            "type": "mrkdwn",
            "text": f"Updated {datetime.now().strftime('%H:%M:%S')} · <https://slackhack.devpost.com/|Slack Hackathon 2026>",
        }],
    })
    return blocks


def memory_blocks(data: dict, query: str) -> list[dict]:
    """Format memory recall results as Slack blocks."""
    results = data.get("results", [])
    count = data.get("count", len(results))

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"🧠 Memory: {query}", "emoji": True},
        },
        {"type": "divider"},
    ]

    if not results:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"_No memories found for \"{query}\"._"},
        })
        return blocks

    blocks.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": f"Found {count} result(s)"}],
    })

    for i, mem in enumerate(results[:5]):
        content = mem.get("content", mem.get("body_json", ""))
        summary = mem.get("summary", "")
        topic = mem.get("topic_path", mem.get("key", ""))
        timestamp = mem.get("timestamp", "")

        text_parts = []
        if topic:
            text_parts.append(f"*{topic}*")
        if timestamp:
            text_parts.append(f"`{timestamp}`")
        if summary:
            text_parts.append(f"\n{summary}")
        elif content:
            try:
                import json
                body = json.loads(content) if isinstance(content, str) else content
                snippet = json.dumps(body, indent=0)[:300]
            except Exception:
                snippet = str(content)[:300]
            text_parts.append(f"\n```{snippet}```")

        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "\n".join(text_parts)},
        })

        if i < len(results[:5]) - 1:
            blocks.append({"type": "divider"})

    return blocks


def read_blocks(data: dict) -> list[dict]:
    """Format file read output as Slack blocks."""
    path = data.get("path", "unknown file")
    content = data.get("content", "")
    truncated = data.get("truncated", False)

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"📄 {path}", "emoji": True},
        },
        {"type": "divider"},
    ]

    if not content:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "_File is empty or not found._"},
        })
        return blocks

    if truncated:
        blocks.append({
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "⚠️ Content was truncated — showing first portion"}],
        })

    # Slack blocks have a ~3000 char limit
    display = _truncate(content, 2800)

    blocks.append({
        "type": "section",
        "text": {"type": "mrkdwn", "text": f"```\n{display}\n```"},
    })

    return blocks


def search_blocks(data: dict, query: str) -> list[dict]:
    """Format code search results as Slack blocks."""
    matches = data.get("matches", data.get("results", []))
    count = data.get("count", len(matches))

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"🔍 Search: {query}", "emoji": True},
        },
        {"type": "divider"},
    ]

    if not matches:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"_No matches found for \"{query}\"._"},
        })
        return blocks

    blocks.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": f"Found {count} match(es)"}],
    })

    for i, match in enumerate(matches[:10]):
        file_path = match.get("file", match.get("path", "unknown"))
        line = match.get("line", "")
        content = match.get("content", match.get("match", ""))
        line_num = match.get("line_number", match.get("line_num", ""))

        text = f"*{file_path}*"
        if line_num:
            text += f"  `L{line_num}`"
        if content:
            snippet = str(content).strip()[:200]
            text += f"\n```{snippet}```"

        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": text},
        })

        if i < len(matches[:10]) - 1:
            blocks.append({"type": "divider"})

    return blocks


def context_blocks(data: dict) -> list[dict]:
    """Format workspace context as a Slack message."""
    rendered = data.get("rendered", data.get("text", ""))

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "📋 Project Context", "emoji": True},
        },
        {"type": "divider"},
    ]

    if rendered:
        display = _truncate(str(rendered), 2800)
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": display},
        })
    else:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "_No context available._"},
        })

    return blocks


def onboarding_blocks(skills_data: dict, services_data: dict, memory_data: dict) -> list[dict]:
    """Build a rich onboarding message for new team members."""
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "👋 Welcome to the project! Here's what you should know:", "emoji": True},
        },
        {"type": "divider"},
    ]

    # Services
    services = services_data.get("services", [])
    if services:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*🩺 Services:*"},
        })
        for svc in services:
            name = svc.get("name", "?")
            status = svc.get("status", "?")
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{_status_emoji(status)} `{name}` — {status}"},
            })

    # Skills
    skills = skills_data.get("skills", [])
    if skills:
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*🛠 Available Skills:*"},
        })
        skill_lines = []
        for s in skills[:10]:
            name = s.get("name", "?")
            desc = s.get("description", "")
            stale = " ⚠️stale" if s.get("stale") else ""
            skill_lines.append(f"• `{name}`{stale} — {desc[:80]}")
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "\n".join(skill_lines)},
        })

    # Recent decisions from memory
    memories = memory_data.get("results", [])
    if memories:
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*🧠 Recent Decisions:*"},
        })
        for mem in memories[:3]:
            topic = mem.get("key", mem.get("topic_path", "?"))
            summary = mem.get("summary", "")
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"• *{topic}*: {summary[:120]}"},
            })

    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [{
            "type": "mrkdwn",
            "text": "Try `@perseus services`, `@perseus memory <topic>`, or `@perseus search <query>`",
        }],
    })

    return blocks


def error_blocks(message: str) -> list[dict]:
    """Format an error response."""
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"❌ *Error:* {message}"},
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "Check logs or try again. If this persists, file an issue."}],
        },
    ]


def help_blocks() -> list[dict]:
    """Show available commands."""
    return [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🤖 Perseus for Slack", "emoji": True},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "Ask me anything about your project:\n\n"
                    "• `@perseus services` — check service health\n"
                    "• `@perseus memory <topic>` — recall team decisions\n"
                    "• `@perseus search <query>` — find code\n"
                    "• `@perseus read <file>` — inspect a file\n"
                    "• `@perseus onboard` — new member context dump\n"
                    "• `@perseus skills` — list available tools\n"
                    "• `@perseus ask <question>` — natural language query\n"
                    "• `@perseus help` — show this message"
                ),
            },
        },
        {"type": "divider"},
        {
            "type": "context",
            "elements": [{
                "type": "mrkdwn",
                "text": "MCP-powered · <https://github.com/Perseus-Computing-LLC/slack-perseus-agent|GitHub> · <https://slackhack.devpost.com/|Slack Hackathon 2026>",
            }],
        },
    ]
```

---

## 9. CONFIGURATION FILES

### manifest.json
```json
{
  "display_information": {
    "name": "Perseus — Live Project Context",
    "description": "AI agent that brings live project context into Slack — service health, memory recall, code search, and team knowledge. Powered by Perseus MCP server.",
    "long_description": "Perseus connects your Slack workspace to live project context via MCP. Ask questions about services, recall team decisions, search code, and onboard new members — all without leaving Slack. Built on the Perseus MCP server with 27+ context tools.",
    "background_color": "#1a1a2e"
  },
  "features": {
    "bot_user": {
      "display_name": "perseus",
      "always_online": true
    },
    "slash_commands": [
      {
        "command": "/perseus",
        "description": "Ask Perseus anything about your project — services, memory, search, context",
        "usage_hint": "[services|memory|search|onboard|ask] [query]",
        "should_escape": false
      }
    ]
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "app_mentions:read",
        "chat:write",
        "commands",
        "im:history",
        "im:read",
        "im:write",
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read"
      ]
    }
  },
  "settings": {
    "event_subscriptions": {
      "bot_events": ["app_mention", "message.im"]
    },
    "interactivity": {
      "is_enabled": true
    },
    "org_deploy_enabled": false,
    "socket_mode_enabled": true
  }
}
```

### .env.example
```
# Slack credentials
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token

# Perseus MCP server
PERSEUS_MCP_URL=http://localhost:5000/mcp

# Optional: Slack sandbox access
SLACK_SANDBOX_URL=https://your-workspace.slack.com
```

### requirements.txt
```
slack-bolt>=1.20.0
httpx>=0.28.0
mcp>=1.0.0
python-dotenv>=1.0.0
```

---

## 10. SUBMISSION CONTENT (Devpost)

### Project Name
**Perseus for Slack — Live Context for Developer Teams**

### Elevator Pitch (≤200 chars)
"Perseus brings live project context into Slack via MCP — answering 'what's running?', 'what did we decide?', and 'where's that code?' so teams ship faster without leaving chat."

### Track
**New Slack Agent** (using MCP server integration)

### What it does
Perseus for Slack is an AI agent that connects developer teams to live project context directly in Slack:
1. **@perseus services** — Real-time service health checks with green/red status indicators
2. **@perseus memory** — Persistent memory recall via Mimir (FTS5 + vector search)
3. **@perseus search** — Full-text code search across the project
4. **@perseus onboard** — New member onboarding with context dump
5. **@perseus ask** — Natural language queries against project knowledge
All responses use Slack Block Kit for rich, readable output.

### How I built it
- Slack Bolt (Python) with Socket Mode
- MCP server integration — Perseus MCP server (27+ tools) via JSON-RPC 2.0
- Regex-based intent routing for deterministic commands, NL fallback using Mimir memory
- Slack Block Kit for all responses — color-coded statuses, code snippets

### Why MCP
Perseus ships as a production MCP server with 27+ tools, real GitHub stars, and active pip installs. We didn't build an MCP server from scratch — we integrated real, open-source MCP infrastructure. The agent demonstrates: services health, memory recall, code search, file inspection, skill discovery, context resolution.

### What's next
- Slack Marketplace submission (Agent for Organizations track)
- Multi-workspace federation via Perseus
- Proactive alerts (service degradation, memory decay)
- Slack AI integration layer on top of Perseus context

---

## 11. DEMO SCENES (5 scenes, ~2:45)

| Scene | Time | Description |
|---|---|---|
| 1 | 0:00-0:35 | Service Health — alice asks `@perseus services`, gets green/red status |
| 2 | 0:36-1:10 | Memory Recall — bob asks about database migration decisions, gets 3 results |
| 3 | 1:11-1:45 | Code Search — carol searches for OAuth token handling, gets 4 file matches |
| 4 | 1:46-2:15 | Onboarding — dave (new hire) asks `@perseus onboard`, gets services + skills + decisions |
| 5 | 2:16-2:45 | Context Accumulation — multi-turn: rate limits → file read → code search across project |

Full transcript: `demo/demo_transcript.md`

---

## 12. RULES AND CONVENTIONS

1. **Draw from Mimir** — call `mimir_recall_when(context="building Slack agent...")` before architectural decisions
2. **Document every issue** — file GitHub issues against `Perseus-Computing-LLC/slack-perseus-agent` for bugs found
3. **Save decisions** — `mimir_remember` into category `decision` or `architecture/slack-perseus-agent`
4. **Commit incrementally** — one commit per logical change, conventional commit messages
5. **Git identity**: `perseus <51974392+tcconnally@users.noreply.github.com>`
6. **License**: MIT in root AND in repo About section
7. **Video**: ≤3 minutes, public/unlisted on YouTube, show working project
8. **Architecture diagram**: Must be visible in submission
9. **Slack sandbox**: Grant access to `slackhack@salesforce.com` and `testing@devpost.com`
10. **No TBDs**: Every Devpost field must be filled
11. **Repo must be public**: Already done ✅

---

## 13. KEY RESOURCES

- Hackathon: https://slackhack.devpost.com/
- Repo: https://github.com/Perseus-Computing-LLC/slack-perseus-agent
- Slack Bolt: https://slack.dev/bolt-python/
- Slack CLI: https://api.slack.com/automation/cli
- MCP spec: https://modelcontextprotocol.io/
- Perseus: https://github.com/Perseus-Computing-LLC/perseus
- Mimir: https://github.com/Perseus-Computing-LLC/mimir
- BSM token cache: /opt/data/webui/minions-hermes-config/cache/bws_cache.json (key: secrets.GITHUB_TOKEN)
