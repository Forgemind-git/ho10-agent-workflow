# Sample 03 — Daily Ops Data Pipeline

**Problem:** Operations teams spend the first hour of every day manually pulling reports, checking spreadsheets, and figuring out what went wrong yesterday. By the time they've identified an anomaly, hours have passed and the damage has compounded.

**This workflow solves it** by composing three pieces:

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Data Pull MCP | Data Gatherer | Pulls yesterday's operational metrics from an API, database, or Google Sheet |
| Skill — Ops Analyst | Shaper | Analyses the data, compares against baselines, and flags anomalies with severity ratings |
| Connector — Slack Notification | Actor | Posts a formatted daily briefing to the ops Slack channel with anomaly highlights |

## The Three Pieces

### MCP: Data Pull MCP
Connects to your data sources — internal APIs, PostgreSQL, Google Sheets, or CSV exports — and fetches the day's operational metrics. Returns a structured dataset ready for analysis.

See `mcp-config.json` for the server config.

### Skill: Ops Analyst
A Claude skill that reads the day's metrics, compares them against 7-day and 30-day baselines, identifies anomalies using configurable thresholds, and writes a plain-English summary with recommended actions.

See `skill.md` for the full skill definition.

### Connector: Slack Notification Connector
Formats the analysis as a Slack Block Kit message and posts it to your ops channel. Uses colour-coded severity (green/yellow/red) and includes a link to the raw data.

See `connector.md` for setup instructions.

## Files in this Sample

```
sample-03/
├── README.md          ← this file
├── workflow.md        ← full step-by-step flow with ASCII diagram
├── skill.md           ← Claude skill definition for Ops Analyst
├── connector.md       ← Slack notification connector setup guide
├── mcp-config.json    ← MCP server configuration snippet
└── sample_run.txt     ← complete log of one successful run
```

## Quick Start

1. Configure your data pull MCP using `mcp-config.json`
2. Add the skill from `skill.md` to your Claude Code project
3. Set up the Slack connector from `connector.md`
4. Schedule the workflow to run at 07:00 daily (see `workflow.md`)

## Expected Output

A Slack message in your ops channel within ~35 seconds of the trigger, with colour-coded anomaly flags, plain-English analysis, and recommended actions for the team.
