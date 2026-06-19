# Demo Script — Perseus for Slack

**Duration:** ~2:45 | **Format:** Terminal-style HTML simulation → Playwright → MP4

## Scene 1: Service Health (0:00–0:35)

**On screen:** Slack channel #engineering with messages appearing
**Narration:** "Every developer has asked 'is the thing running?' Perseus answers that without leaving Slack."

```
👤 alice  10:23 AM
@perseus services

🤖 perseus  10:23 AM
🩺 Service Health
────────────────
🟢 Hermes WebUI — up (19ms)
🟢 Minions — running
🟢 Hermes Agent — running
⚪ Docker — not available
```

## Scene 2: Memory Recall (0:36–1:10)

**On screen:** Slack thread in #eng-architecture
**Narration:** "Teams make dozens of decisions. Perseus remembers them all."

```
👤 bob  10:25 AM
@perseus memory database migration strategy

🤖 perseus  10:25 AM
🧠 Memory: database migration strategy
────────────────
Found 3 results

*migration-strategy-v2*
2026-06-10
"Decided on phased migration: SQLite → PostgreSQL with dual-write period"

*connector-migration*
2026-06-08
"Perseus connector swap procedure documented — run before any new deploy"

*db-decay-bug*
2026-06-05
"Fixed decay score recalc bugs in Mimir v0.5 — always run cohere after backup"
```

## Scene 3: Code Search (1:11–1:45)

**On screen:** #dev channel, code search response
**Narration:** "Where's that OAuth logic? Perseus finds it instantly."

```
👤 carol  10:28 AM
@perseus search OAuth token handling

🤖 perseus  10:28 AM
🔍 Search: OAuth token handling
────────────────
Found 4 matches

*src/gateway/auth.py*  L42
def get_oauth_token(provider: str) -> str:

*src/tools/mcp_oauth.py*  L15
class MCPOAuthManager:

*src/cli/login.py*  L78
token = exchange_code(code, redirect_uri)

*config.yaml*  L120
oauth:
  providers:
```

## Scene 4: Onboarding (1:46–2:15)

**On screen:** New hire `dave` joins #general, types `@perseus onboard`
**Narration:** "New team member? Perseus gets them up to speed in seconds."

```
👤 dave  10:31 AM
@perseus onboard

🤖 perseus  10:31 AM
👋 Welcome to the project! Here's what you should know:

🩺 Services:
🟢 Hermes WebUI — up (19ms)
🟢 Minions — running
🟢 Hermes Agent — running

🛠 Available Skills:
• github-pr-workflow — PR lifecycle
• hackathon-submission — Devpost entry workflow
• perseus-context — Live context directives

🧠 Recent Decisions:
• Use postgres-16 for all new deployments
• Mimir encryption enabled at rest
• CI requires rebuilt perseus.py after src changes
```

## Scene 5: Context Accumulation (2:16–2:45)

**On screen:** Multi-message thread showing contextual awareness
**Narration:** "Perseus remembers what your team is working on and surfaces relevant context automatically."

```
👤 alice  10:35 AM
@perseus what API rate limits did we set last week?

🤖 perseus  10:35 AM
🧠 Memory: API rate limits
Found: "Rate limits set to 100 req/min for free tier, 1000/min for pro — 
decided 2026-06-12. Config in gateway/rate_limiter.py"

👤 alice  10:36 AM
@perseus show me that file

🤖 perseus  10:36 AM
📄 gateway/rate_limiter.py
```python
DEFAULT_TIER_LIMITS = {
    "free": 100,
    "pro": 1000,
    ...
```

👤 bob  10:37 AM
@perseus search all files referencing DEFAULT_TIER_LIMITS

🤖 perseus  10:37 AM
🔍 Search: DEFAULT_TIER_LIMITS
Found 3 matches...
```

---

## Recording Notes

- Font: JetBrains Mono, 14px
- Colors: user = #d4d4d4, bot = #7ebae4, system = #b4a0e5
- Background: #1a1a2e (Slack dark theme)
- Simulate with HTML + CSS, auto-scrolling terminal
- Playwright: 1280x720, headless chromium
- FFmpeg: WebM → MP4, h264, crf 23
