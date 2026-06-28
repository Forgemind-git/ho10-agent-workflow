# Cowork Playbook — Content Pipeline

## Overview

This playbook connects all three components of the content pipeline workflow end-to-end.

```
MCP: fetch_sources(topic)
        ↓
Skill: draft_article(brief)
        ↓
Cowork: review + schedule for publishing
```

## Step 1 — Set up the MCP server

1. Navigate to `mcp-server/`
2. TODO: Add your setup steps (install dependencies, configure credentials, run server)
3. Verify the MCP tool is reachable from Claude Desktop

## Step 2 — Create the Skill in Claude.ai

1. Go to claude.ai → Skills → New Skill
2. Name it: TODO (e.g. "Content Draft Writer")
3. Paste the prompt from `skill-template.md`
4. TODO: Add any required integrations or permissions
5. Save and test with a sample input

## Step 3 — Start a Cowork session

1. Open Claude.ai and start a new Cowork session
2. TODO: Describe which agents / roles to add to the Cowork
3. TODO: Describe the handoff format between agents

## Step 4 — Run the full workflow

1. Trigger: TODO (e.g. "Research and draft an article about [topic]")
2. MCP fetches sources → passes to Skill
3. Skill drafts article → presents to Cowork for review
4. TODO: Describe what the reviewer checks before publishing
5. TODO: Describe how the final output is delivered or scheduled

## Checklist

- [ ] MCP server running and tested
- [ ] Skill created and returning correct format
- [ ] Cowork session configured with correct agents
- [ ] Full end-to-end run completed at least once
- [ ] Output reviewed and published / filed
