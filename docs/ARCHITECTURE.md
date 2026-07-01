# Architecture — Perseus for Slack

## Overview

Perseus for Slack is a Slack agent that connects developer teams to live project context via the Model Context Protocol (MCP). It bridges Slack's conversational interface with Perseus's context resolution engine, enabling teams to query services, recall decisions, search code, and onboard new members without leaving Slack.

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Slack Workspace                        │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ @mention │  │ /slash   │  │    DM    │               │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│       │              │              │                     │
│       └──────────────┼──────────────┘                     │
│                      │                                    │
│              ┌───────▼────────┐                           │
│              │  Slack Bolt    │  Python / asyncio         │
│              │  (Socket Mode) │                           │
│              └───────┬────────┘                           │
└──────────────────────┼──────────────────────────────────┘
                       │
                       │ Intent Routing
                       │
              ┌────────▼────────┐
              │   Handlers      │
              │  ─────────────  │
              │  services       │
              │  memory         │
              │  search         │
              │  read           │
              │  onboard        │
              │  ask (NL)       │
              └────────┬────────┘
                       │
                       │ MCP JSON-RPC 2.0
                       │ (HTTP transport)
                       │
              ┌────────▼────────────────────────────┐
              │         Perseus MCP Server           │
              │  ┌─────────────────────────────────┐ │
              │  │  27+ Context Tools               │ │
              │  ├─────────────────────────────────┤ │
              │  │ perseus_services    ── health    │ │
              │  │ perseus_memory      ── recall    │ │
              │  │ perseus_read        ── files     │ │
              │  │ perseus_list        ── browse    │ │
              │  │ perseus_skills      ── skill list│ │
              │  │ perseus_context     ── full ctx  │ │
              │  │ perseus_session     ── history   │ │
              │  │ perseus_inbox       ── messages  │ │
              │  │ ...                             │ │
              │  └─────────────────────────────────┘ │
              │                                     │
              │  ┌─────────────────────────────────┐ │
              │  │ Backends                        │ │
              │  ├─────────────────────────────────┤ │
              │  │ Perseus Vault (persistent memory) │ │
              │  │  • FTS5 + vector hybrid search   │ │
              │  │  • Ebbinghaus decay              │ │
              │  │  • AES-256-GCM encryption        │ │
              │  │                                  │ │
              │  │ Workspace (file system)           │ │
              │  │  • AGENTS.md context              │ │
              │  │  • Config files                   │ │
              │  │  • Session history                │ │
              │  └─────────────────────────────────┘ │
              └──────────────────────────────────────┘
```

## Data Flow

1. **User sends message** — @mention, slash command, or DM in Slack
2. **Slack Bolt receives event** — Socket Mode handler dispatches to async handler
3. **Intent parsing** — Regex-based routing maps message to one of 10+ intents
4. **MCP call** — PerseusHandler calls `perseus_<tool>` via JSON-RPC 2.0 over HTTP
5. **Perseus resolves** — Directive engine executes the request against workspace/memory backends
6. **Blocks formatter** — Raw JSON output → rich Slack Block Kit message
7. **Response posted** — Formatted blocks appear in the Slack channel/thread

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Socket Mode** over HTTP endpoints | No public URL needed for development. Works in sandbox. |
| **Slack Bolt (Python)** over Slack CLI | Bolt is battle-tested, well-documented, and works with existing Python tooling. |
| **HTTP MCP transport** over stdio | Allows Perseus server to run independently. Easier in container/cloud setups. |
| **Intent routing** over LLM for routing | Deterministic, fast, no token cost for basic queries. NL fallback uses memory recall. |
| **Slack Blocks** over plain text | Rich formatting improves readability. Color-coded statuses, code blocks, structured layouts. |
| **Async throughout** | Slack Bolt is async-native. MCP client uses httpx.AsyncClient. No blocking I/O. |
| **Client-side code search** (`perseus_list` + `perseus_read` + grep) | Perseus exposes no server-side search tool, so the agent composes one: enumerate files via `perseus_list`, fetch candidates via `perseus_read`, and match in Python. Bounded (≤40 files, ≤60 matches, depth ≤4) to cap round-trips. |

## Technology Stack

- **Slack:** Bolt for Python, Socket Mode, Block Kit
- **MCP:** Model Context Protocol 2025-06-18, JSON-RPC 2.0
- **Perseus:** Live context engine v1.0.6, 27+ MCP tools
- **Perseus Vault:** Persistent memory with FTS5 + vector search
- **Python:** 3.11+, asyncio, httpx
- **Demo:** Playwright, FFmpeg, HTML/CSS terminal simulation

## Security

- Slack tokens stored in `.env` (never committed)
- MCP connection over localhost (not exposed publicly)
- Socket Mode avoids exposing HTTP endpoints
- Perseus MCP tools respect `tool_allowlist`/`tool_blocklist` config
- Sensitive tools (`perseus_query`, `perseus_agent`) require explicit opt-in
