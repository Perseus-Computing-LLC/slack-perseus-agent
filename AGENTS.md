# Project Context — Perseus for Slack

## What this is
A Slack agent that connects developer teams to live project context via MCP. Built for the Slack Agent Builder Challenge 2026 (New Slack Agent track, $42K prize pool, July 13 deadline).

## How it works
Slack user → Slack Bolt (Python, Socket Mode) → Perseus MCP server (JSON-RPC 2.0 over HTTP) → workspace/memory backends → formatted Slack Blocks response.

## Key files
- `src/app.py` — Slack Bolt app entry point
- `src/mcp_client.py` — JSON-RPC MCP client for Perseus
- `src/handlers.py` — Intent routing (services, memory, search, read, onboard, ask)
- `src/blocks.py` — Slack Block Kit formatters

## Build rules
- Use `sync` not async unless existing async infrastructure
- Prefer Slack Blocks over plain text for all responses
- Every MCP call should have a fallback error block
- Intent routing is regex-based; NL fallback uses memory recall
- Demo is a terminal HTML simulation → Playwright → MP4

## Hackathon resources
- Devpost: https://slackhack.devpost.com/
- Deadline: July 13, 2026 5pm PT
- Track: New Slack Agent (MCP server integration)
- Prize: $42,000 + Dreamforce trip
- Requirements: ~3 min demo video, architecture diagram, Slack sandbox URL, GitHub repo

## Repo
- GitHub: https://github.com/Perseus-Computing-LLC/slack-perseus-agent
- License: MIT
- Owner: Perseus Computing LLC

## Perseus MCP tools used
- `perseus_services` — service health
- `perseus_memory` — Mneme recall
- `perseus_mimir` — direct FTS5 memory
- `perseus_read` — file inspection
- `perseus_list` — directory enumeration (also powers client-side code search)
- `perseus_skills` — skill listing
- `perseus_context` — workspace context
- `perseus_session` — session history
- `perseus_inbox` — messages
