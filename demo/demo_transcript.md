# Demo Transcript — Perseus for Slack

This transcript simulates a realistic Slack conversation showing Perseus in action across 5 scenes.

---

## Scene 1: Service Health (0:00–0:35)

```
#engineering  10:23 AM

alice
@perseus services

Perseus APP  10:23 AM
🩺 Service Health
━━━━━━━━━━━━━━━━━━
🟢 Hermes WebUI — up (19ms)
🟢 Minions — running
🟢 Hermes Agent — running
⚪ Docker — not available
━━━━━━━━━━━━━━━━━━
Updated 10:23:45 · Slack Hackathon 2026

alice
nice, everything looks good for the demo
```

---

## Scene 2: Memory Recall (0:36–1:10)

```
#eng-architecture  10:25 AM

bob
@perseus memory database migration strategy

Perseus APP  10:25 AM
🧠 Memory: database migration strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found 3 results

*migration-strategy-v2*
2026-06-10
"We decided on phased migration: SQLite → PostgreSQL
with dual-write period during transition"

*connector-migration*
2026-06-08
"Perseus connector swap procedure documented.
Run before any new deployment."

*db-decay-bug*
2026-06-05
"Fixed decay score recalculation bugs in Mimir v0.5.
Always run cohere after backup."

bob
perfect, exactly what I needed. the dual-write period
was what I was trying to remember
```

---

## Scene 3: Code Search (1:11–1:45)

```
#dev  10:28 AM

carol
@perseus search OAuth token handling

Perseus APP  10:28 AM
🔍 Search: OAuth token handling
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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

carol
thanks! i need to update the token refresh logic
```

---

## Scene 4: Onboarding (1:46–2:15)

```
#general  10:31 AM

dave has joined #general

dave
hey everyone! just joined. @perseus onboard

Perseus APP  10:31 AM
👋 Welcome to the project! Here's what you should know:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🩺 Services:
🟢 Hermes WebUI — up (19ms)
🟢 Minions — running
🟢 Hermes Agent — running

🛠 Available Skills:
• github-pr-workflow — PR lifecycle
• hackathon-submission — Devpost entry workflow
• perseus-context — Live context directives
• systematic-debugging — Root cause analysis

🧠 Recent Decisions:
• Use postgres-16 for all new deployments
• Mimir encryption enabled at rest (AES-256-GCM)
• CI requires rebuilt perseus.py after src/ changes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Try @perseus services, @perseus memory <topic>, or @perseus search <query>

dave
awesome, this is super helpful! 🚀
```

---

## Scene 5: Context Accumulation (2:16–2:45)

```
#engineering  10:35 AM

alice
@perseus what API rate limits did we set last week?

Perseus APP  10:35 AM
🧠 Memory: API rate limits
━━━━━━━━━━━━━━━━━━━━━━━━
"Rate limits set to 100 req/min for free tier,
1000/min for pro — decided 2026-06-12.
Config in gateway/rate_limiter.py"

alice
@perseus show me gateway/rate_limiter.py

Perseus APP  10:36 AM
📄 gateway/rate_limiter.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEFAULT_TIER_LIMITS = {
    "free": 100,
    "pro": 1000,
    "enterprise": 10000,
}

bob
@perseus search all files referencing DEFAULT_TIER_LIMITS

Perseus APP  10:37 AM
🔍 Search: DEFAULT_TIER_LIMITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found 3 matches

*gateway/rate_limiter.py*  L14
DEFAULT_TIER_LIMITS = {

*api/middleware.py*  L42
from gateway.rate_limiter import DEFAULT_TIER_LIMITS

*tests/test_rate_limit.py*  L8
from gateway.rate_limiter import DEFAULT_TIER_LIMITS

alice
@perseus memory when did we decide on the enterprise tier?

Perseus APP  10:38 AM
🧠 Memory: enterprise tier decision
"Enterprise tier added 2026-06-14 with 10,000 req/min
and priority support SLA. See docs/pricing.md"
```

---

## End Screen

```
Perseus for Slack
Live context for developer teams

🔗 github.com/Perseus-Computing-LLC/slack-perseus-agent
🏆 Slack Agent Builder Challenge 2026
📋 New Slack Agent track (MCP integration)

Built with ❤️ by Perseus Computing LLC
MIT License
```
