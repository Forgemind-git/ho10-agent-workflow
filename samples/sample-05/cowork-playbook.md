# Cowork Playbook — Morning Briefing

## Overview

This playbook connects all three components of the morning briefing workflow end-to-end.

```
MCP: get_morning_inputs()
        ↓
Skill: write_briefing(inputs)
        ↓
Cowork: output formatted daily briefing
```

## Step 1 — Set up the MCP server

1. Navigate to `mcp-server/`
2. TODO: Add your setup steps (install dependencies, configure credentials, run server)
3. Verify the MCP tool is reachable from Claude Desktop

## Step 2 — Create the Skill in Claude.ai

1. Go to claude.ai → Skills → New Skill
2. Name it: TODO (e.g. "Morning Briefing Writer")
3. Paste the prompt from `skill-template.md`
4. TODO: Add any required integrations or permissions
5. Save and test with a sample input

## Step 3 — Start a Cowork session

1. Open Claude.ai and start a new Cowork session
2. TODO: Describe which agents / roles to add to the Cowork
3. TODO: Describe the handoff format between agents

## Step 4 — Run the full workflow

1. Trigger: TODO (e.g. "Generate my morning briefing for today")
2. MCP pulls calendar, emails, and tasks → passes to Skill
3. Skill writes priority list + 3 key actions → presents to Cowork
4. TODO: Describe how the briefing is reviewed or auto-delivered
5. TODO: Describe the delivery format (chat message, email, notification)

## Checklist

- [ ] MCP server running and tested
- [ ] Skill created and returning correct format
- [ ] Cowork session configured with correct agents
- [ ] Full end-to-end run completed at least once
- [ ] Morning briefing delivered in chosen format
