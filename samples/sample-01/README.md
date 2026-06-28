# HO10 Sample 01 — Content Creation Pipeline

## What you'll build
A hands-off content pipeline that takes one trigger — "draft today's post" — and runs three steps for you: it **finds** a trending topic in your industry, **writes** a post in your brand voice, and **publishes** it (or drops it ready to send). You assemble it entirely inside Claude.ai using a Skill, a Connector, and an MCP — no coding, no servers to babysit.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team).

1. Open **Claude.ai** and go to **Skills** (`claude.ai/skills`). Click **New Skill**, name it `brand-voice-writer`, and paste in the full text from **`skill.md`** in this folder. Save it. This teaches Claude your post style.
2. Go to **Settings → Connectors** (`claude.ai/settings/connectors`) and turn on the connector for where you publish — for example **LinkedIn** or **X/Twitter**. You click **Connect** and sign in once; Claude handles the rest. (This is the easy version of `connector.md`.)
3. For the trend research step, open **Claude Desktop** (`claude.ai/download`), open its config, and paste the entry from **`mcp-config.json`** so Claude can pull trending topics. Restart Claude Desktop. *(Optional — you can skip this and just tell Claude the topic yourself.)*
4. Start a new chat and paste **the example prompt** below. Claude chains all three steps and shows you the post before it goes out.

## The example prompt
Copy this into a new Claude chat:

```
You are running my content pipeline. Do all three steps in order and show me the result of each:

1. RESEARCH: Find the top trending topic in "AI for small businesses" right now (use the trend-research MCP if available; otherwise suggest one based on what you know).
2. DRAFT: Use my brand-voice-writer skill to write a LinkedIn post about that topic. Brand = "Forgemind AI", audience = founders and ops leads at 10–200 person companies. Give me one main version plus a shorter version.
3. PUBLISH: Show me the post and ask for my approval. Once I say "post it", publish it to LinkedIn using my connected LinkedIn connector and give me the live link.

Stop and wait for my approval before publishing.
```

## The three pieces

| Piece | Role | What it does |
|-------|------|-------------|
| MCP — Trend Research | Data gatherer | Surfaces trending topics in your industry |
| Skill — Brand Voice Writer | Shaper | Drafts a post in your exact voice (see `skill.md`) |
| Connector — LinkedIn / X | Actor | Publishes the post and returns the live link |

## Files in this sample

- `skill.md` — the Brand Voice Writer skill (paste into Claude → Skills)
- `workflow.md` — the full flow with a diagram and step-by-step detail
- `connector.md` — how the publishing connector works (advanced/manual setup)
- `mcp-config.json` — the MCP server entry for Claude Desktop
- `sample_run.txt` — a real end-to-end run you can read through
- `index.html` — open in your browser for a clickable setup guide

## Make it your own
- Edit the Skill to include your real brand name, audience, and 2–3 example posts — the more specific, the closer Claude matches your voice.
- Swap the topic area in the prompt (e.g. "fintech", "climate tech") for your niche.
- Change step 3 to "save as a draft" instead of "publish" while you build trust in the output.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. `connector.md` and `mcp-config.json` show the fuller manual setup (OAuth apps, running the MCP server, scheduling a daily run). That path uses platform API keys and a terminal, and is only worth it once you want this running unattended every morning.
