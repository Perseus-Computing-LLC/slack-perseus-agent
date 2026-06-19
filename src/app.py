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
if not SLACK_APP_TOKEN or SLACK_APP_TOKEN.startswith("xapp-y"):
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
