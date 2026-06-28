# Cowork Playbook — Support Workflow

## Overview

This playbook connects all three components of the support workflow end-to-end.

```
MCP: get_ticket(id)
        ↓
Skill: draft_reply(ticket)
        ↓
Cowork: update ticket status + send reply
```

## Step 1 — Set up the MCP server

1. Navigate to `mcp-server/`
2. TODO: Add your setup steps (install dependencies, configure credentials, run server)
3. Verify the MCP tool is reachable from Claude Desktop

## Step 2 — Create the Skill in Claude.ai

1. Go to claude.ai → Skills → New Skill
2. Name it: TODO (e.g. "Support Reply Drafter")
3. Paste the prompt from `skill-template.md`
4. TODO: Add any required integrations or permissions
5. Save and test with a sample input

## Step 3 — Start a Cowork session

1. Open Claude.ai and start a new Cowork session
2. TODO: Describe which agents / roles to add to the Cowork
3. TODO: Describe the handoff format between agents

## Step 4 — Run the full workflow

1. Trigger: TODO (e.g. "Handle support ticket #[ID]")
2. MCP fetches ticket details and history → passes to Skill
3. Skill drafts reply + internal note → presents to Cowork for review
4. TODO: Describe what the reviewer checks before sending
5. TODO: Describe how the ticket status is updated after sending

## Checklist

- [ ] MCP server running and tested
- [ ] Skill created and returning correct format
- [ ] Cowork session configured with correct agents
- [ ] Full end-to-end run completed at least once
- [ ] Ticket status updated and reply sent
