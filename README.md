# HO10 — Composed Agent Workflow

> Hands-on portfolio project · **Week 4** · **Peer-reviewed** · module M11. Part of the **ForgeMind AI — AI Productivity Essentials** course.

You compose three Claude.ai building blocks into one workflow:

- a **Skill** (Claude's instructions for the job),
- a **Connector** (Claude takes an action in another app, e.g. Slack, Gmail, LinkedIn),
- an **MCP** (Claude pulls in fresh data).

One trigger then runs **gather → shape → act** for you.

## Use it with your Claude.ai subscription
**No API key needed.** Everything runs on your normal Claude.ai login (Pro or Team), plus the free Claude Desktop app if you want the MCP step.

1. Open a sample below and read its `README.md`.
2. Follow its **"Use it with your Claude.ai subscription"** steps — paste the Skill into Claude → Skills, turn on the Connector in Settings → Connectors, and (optionally) add the MCP in Claude Desktop.
3. Paste the sample's ready-made example prompt into a new Claude chat and watch it run.

Each sample is **copy-and-use**: the Skill, the example prompt, and a real sample run are all filled in. Start from one, then tweak it for your own work.

## The 5 samples

| # | Sample | One trigger does… |
|---|--------|-------------------|
| 01 | [Content Creation Pipeline](samples/sample-01/) | research a trend → draft a post in your voice → publish it |
| 02 | [Lead Enrichment & Outreach](samples/sample-02/) | enrich a lead → draft a personalised email → log it to your CRM |
| 03 | [Daily Ops Data Pipeline](samples/sample-03/) | pull yesterday's metrics → flag anomalies → post to Slack |
| 04 | [Support Ticket Workflow](samples/sample-04/) | fetch a ticket → draft a reply → update the tracker |
| 05 | [Personal Morning Briefing](samples/sample-05/) | gather calendar + email + news → summarise → deliver your brief |

Open `index.html` in your browser for a clickable overview of all five.

## What to ship (for the hands-on)
Pick one sample (or bring your own use case), assemble the Skill + Connector + MCP in your Claude.ai subscription, run it end-to-end, and record the run.

## Optional — automate it (advanced)
Each sample's `connector.md` and `mcp-config.json` show the fuller manual setup for running unattended on a schedule. That path uses platform API keys and a terminal and is **not required** for the course.

---

*HO10 · Peer-reviewed · ForgeMind AI Course · module M11 (Week 4)*
