# Devpost Submission — Perseus for Slack

## Project Name
**Perseus for Slack — Live Context for Developer Teams**

## Elevator Pitch (≤200 chars)
"Perseus brings live project context into Slack via MCP — answering 'what's running?', 'what did we decide?', and 'where's that code?' so teams ship faster without leaving chat."

## Track
**New Slack Agent** (using MCP server integration)

## What it does
Perseus for Slack is an AI agent that connects developer teams to live project context directly in Slack. It answers five critical questions developers ask every day:

1. **"What services are running?"** — Real-time health checks with green/red status indicators
2. **"What did we decide about X?"** — Persistent memory recall via Perseus Vault (FTS5 + vector search)
3. **"Where is that code?"** — Full-text code search across the project (composed client-side from `perseus_list` + `perseus_read`)
4. **"What should I know about this project?"** — New member onboarding with context dump
5. **"Ask anything"** — Natural language queries against project knowledge

All responses are formatted with Slack Block Kit for rich, readable output.

## How I built it
- **Slack Bolt (Python)** with Socket Mode for no-public-URL development
- **MCP server integration** — Perseus MCP server provides 27+ context resolution tools via JSON-RPC 2.0
- **Intent routing** — Regex-based deterministic routing for common commands, with NL fallback using Perseus Vault memory recall
- **Slack Block Kit** for all responses — color-coded statuses, code snippets, structured layouts
- **Perseus Context Engine** — Live workspace context resolution (services, files, sessions, skills)
- **Perseus Vault Persistent Memory** — FTS5 + vector hybrid search with Ebbinghaus decay

## Why MCP
Perseus ships as a **production MCP server** with 27+ tools, real GitHub stars, and active pip installs. We didn't build an MCP server from scratch for this hackathon — we integrated a real, open-source MCP infrastructure that developers already use. The Slack agent demonstrates:

- `perseus_services` — service health monitoring
- `perseus_memory` — persistent knowledge recall
- `perseus_read` — file inspection
- `perseus_list` — directory enumeration (composed with `perseus_read` for client-side code search)
- `perseus_skills` — capability discovery
- `perseus_context` — workspace context resolution

This is the strongest possible MCP entry: an actual production MCP server powering a real Slack integration.

## What's next
- **Slack Marketplace submission** — Graduate to the Agent for Organizations track
- **Multi-workspace federation** — Cross-project context via Perseus federation
- **Proactive alerts** — Service degradation and memory decay alerts pushed to Slack
- **Slack AI integration** — Layer Slack AI summarization on top of Perseus context
- **More backends** — Git, JIRA, Linear connectors via Perseus extensibility

## Links
- **Demo video:** https://www.youtube.com/watch?v=4fLo_PtEw-I
- **Slack sandbox:** https://perseus.slack.com (collaborators: slackhack@salesforce.com, testing@devpost.com)
- **GitHub:** https://github.com/Perseus-Computing-LLC/slack-perseus-agent
- **Architecture diagram:** [assets/architecture-diagram.png](../assets/architecture-diagram.png)
- **Perseus:** https://github.com/Perseus-Computing-LLC/perseus
- **Perseus Vault:** https://github.com/Perseus-Computing-LLC/perseus-vault
- **Hackathon:** https://slackhack.devpost.com/

## Built by
Perseus Computing LLC — [Thomas Connally](https://github.com/tcconnally)
