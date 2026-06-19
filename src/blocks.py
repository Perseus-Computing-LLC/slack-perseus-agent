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
