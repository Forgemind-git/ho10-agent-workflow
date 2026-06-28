# HO10 Sample 2 — Lead Workflow

## Your task

Your reps waste time enriching leads, writing outreach and logging separately. Build a workflow: MCP enriches, Skill writes, Cowork logs.

## What you will build

A composed workflow connecting: an MCP tool (data fetching) → a Skill (processing/drafting) → Cowork (review + output)

## Components

- MCP tool: `enrich_lead(company_name)` → firmographic data
- Skill: `write_outreach(lead_data)` → personalised email
- Cowork step: log to CRM or sheet

## Build order

1. Build and test the MCP server (see `mcp-server/`)
2. Create the Skill in claude.ai
3. Connect them in a Cowork session
4. Run the full workflow end-to-end

## Required

Claude Desktop (for MCP) + Claude.ai Pro/Team (for Skills + Cowork)
