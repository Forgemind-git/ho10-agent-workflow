# Cowork Playbook — Ops Pipeline

## Overview

This playbook connects all three components of the ops pipeline end-to-end.

```
MCP: fetch_ops_data()
        ↓
Skill: analyse_and_flag(data)
        ↓
Cowork: file report + notify Slack or email
```

## Step 1 — Set up the MCP server

1. Navigate to `mcp-server/`
2. TODO: Add your setup steps (install dependencies, configure credentials, run server)
3. Verify the MCP tool is reachable from Claude Desktop

## Step 2 — Create the Skill in Claude.ai

1. Go to claude.ai → Skills → New Skill
2. Name it: TODO (e.g. "Ops Data Analyser")
3. Paste the prompt from `skill-template.md`
4. TODO: Add any required integrations or permissions
5. Save and test with a sample input

## Step 3 — Start a Cowork session

1. Open Claude.ai and start a new Cowork session
2. TODO: Describe which agents / roles to add to the Cowork
3. TODO: Describe the handoff format between agents

## Step 4 — Run the full workflow

1. Trigger: TODO (e.g. "Run today's ops data pipeline")
2. MCP pulls daily metrics → passes to Skill
3. Skill analyses and flags anomalies → presents to Cowork
4. TODO: Describe what the reviewer checks before routing
5. TODO: Describe how the report is filed and notification is sent

## Checklist

- [ ] MCP server running and tested
- [ ] Skill created and returning correct format
- [ ] Cowork session configured with correct agents
- [ ] Full end-to-end run completed at least once
- [ ] Report filed and Slack/email notification sent
