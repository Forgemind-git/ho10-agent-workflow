# HO10 Sample 3 — Ops Pipeline

## Your task

Your ops routine means pulling data, analysing and filing by hand every day. Build a workflow: MCP pulls, Skill analyses, Cowork routes.

## What you will build

A composed workflow connecting: an MCP tool (data fetching) → a Skill (processing/drafting) → Cowork (review + output)

## Components

- MCP tool: `fetch_ops_data()` → daily metrics
- Skill: `analyse_and_flag(data)` → summary + anomalies
- Cowork step: file report + notify Slack or email

## Build order

1. Build and test the MCP server (see `mcp-server/`)
2. Create the Skill in claude.ai
3. Connect them in a Cowork session
4. Run the full workflow end-to-end

## Required

Claude Desktop (for MCP) + Claude.ai Pro/Team (for Skills + Cowork)
