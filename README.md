# Perseus for Slack — Live Context for Developer Teams

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Slack Agent Builder Challenge](https://img.shields.io/badge/Slack-2026_Hackathon-4A154B?logo=slack)](https://slackhack.devpost.com/)

**Perseus brings live project context into Slack via MCP** — answering "what's running?", "what did we decide?", and "where's that code?" so developer teams ship faster without leaving chat.

Built for the **Slack Agent Builder Challenge 2026** (New Slack Agent track) using **Perseus MCP server integration**.

## What it does

- `@perseus services` — check service health from Slack
- `@perseus memory <topic>` — recall team decisions and context
- `@perseus search <query>` — find code across the project
- `@perseus onboard` — new team member context dump
- `@perseus ask <question>` — natural language project queries

## Architecture

```
Slack User → Slack Agent (Bolt) → MCP → Perseus Server
                                        ├── @services (health)
                                        ├── @memory (Mimir recall)
                                        ├── @read (file inspection)
                                        ├── @search (code search)
                                        └── @query (NL context)
```

## Why MCP

The Slack challenge requires MCP server integration, Slack AI, or Real-Time Search. Perseus ships as a **production MCP server** with 27+ tools for context resolution — we're wiring real infrastructure into Slack, not building a toy.

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env  # fill in SLACK_BOT_TOKEN, PERSEUS_MCP_URL
python src/app.py
```

## Project structure

```
├── src/           # Slack Bolt agent (Python)
│   ├── app.py     # Main app, mentions + slash commands
│   ├── mcp_client.py  # MCP client (Perseus server)
│   ├── handlers.py    # Intent routing
│   └── blocks.py      # Slack Block Kit formatters
├── demo/          # Demo video script + transcript
├── docs/          # Architecture docs + submission
└── assets/        # Architecture diagram
```

## Hackathon

- **Challenge:** [Slack Agent Builder Challenge](https://slackhack.devpost.com/)
- **Track:** New Slack Agent (MCP server integration)
- **Deadline:** July 13, 2026
- **Prize:** $42,000 + Dreamforce trip

## License

MIT — [LICENSE](LICENSE)
