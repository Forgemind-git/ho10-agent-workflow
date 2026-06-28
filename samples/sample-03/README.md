# HO10 Sample 03 — Daily Ops Data Pipeline

## What you'll build
A daily briefing that does the boring first-hour-of-the-day work for you. One trigger **pulls** yesterday's numbers, **analyses** them against your normal baselines to flag anything weird, and **posts** a colour-coded summary to your team's Slack — so problems surface in seconds instead of hours. You assemble it in Claude.ai with a Skill, a Connector, and an MCP.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team).

1. Open **Claude.ai** → **Skills** (`claude.ai/skills`). Click **New Skill**, name it `ops-analyst`, and paste in the full text from **`skill.md`**. Save it. This teaches Claude how to spot and rank anomalies.
2. Go to **Settings → Connectors** (`claude.ai/settings/connectors`) and turn on the **Slack** connector. Click **Connect** and sign in once, then pick the channel it can post to. (Easy version of `connector.md`.)
3. For the data pull, open **Claude Desktop** (`claude.ai/download`) and paste the entry from **`mcp-config.json`** into its config so Claude can fetch your metrics (from a Google Sheet, database, or API). Restart Claude Desktop. *(Optional — you can also paste yesterday's numbers straight into the chat.)*
4. Start a new chat and paste **the example prompt** below. Claude pulls, analyses, and posts the briefing.

## The example prompt
Copy this into a new Claude chat:

```
You are running my daily ops briefing. Do all three steps and show me each result:

1. PULL: Get yesterday's operational metrics (use the data-pull MCP if available; otherwise I'll paste them). I track: orders, revenue, signups, support tickets, and average response time. Include the 7-day average for each.
2. ANALYSE: Use my ops-analyst skill. For every metric, work out the % change vs the 7-day average, label it NORMAL / WARNING / CRITICAL, and note when two metrics look connected (e.g. orders down while tickets spike). Give me one concrete action per anomaly and a 3-sentence executive summary.
3. NOTIFY: Show me the briefing. Once I say "send it", post it to my #ops Slack channel via the Slack connector, with the most critical finding first.

Wait for my approval before posting to Slack.
```

## The three pieces

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Data Pull | Data gatherer | Fetches yesterday's metrics from your source |
| Skill — Ops Analyst | Shaper | Flags anomalies and writes a plain-English summary (see `skill.md`) |
| Connector — Slack | Actor | Posts the briefing to your ops channel |

## Files in this sample

- `skill.md` — the Ops Analyst skill (paste into Claude → Skills)
- `workflow.md` — the full flow with a diagram and step-by-step detail
- `connector.md` — how the Slack connector works (advanced/manual setup)
- `mcp-config.json` — the data-pull MCP entry for Claude Desktop
- `sample_run.txt` — a real end-to-end run you can read through
- `index.html` — open in your browser for a clickable setup guide

## Make it your own
- Edit the Skill to list the exact metrics you care about and which direction is "good" for each.
- Tune the thresholds (the example flags >10% as WARNING, >20% as CRITICAL).
- Swap Slack for an email connector if your team lives in the inbox instead.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `connector.md` and `mcp-config.json` show the fuller manual setup (database credentials, Slack tokens, running the MCP server, a 7:00 schedule). Only worth it once you want the briefing to land every morning untouched.
