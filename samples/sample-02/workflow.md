# Workflow: Lead Enrichment & Outreach

## Overview

This workflow takes a raw lead (name + company domain) and automatically enriches it with real company data, then drafts a personalised cold email using a specific signal — and logs everything to the CRM.

**Trigger options:**
- Manual: `node run-workflow.js lead-workflow --email john@acme.com`
- Webhook: POST to `/webhook/lead-workflow` with lead data
- CRM automation: triggered when a new contact is added with status "new"
- Batch: CSV of leads processed sequentially

**Duration:** ~20–30 seconds per lead

---

## ASCII Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                LEAD ENRICHMENT & OUTREACH WORKFLOW              │
└─────────────────────────────────────────────────────────────────┘

  [TRIGGER]
  New lead added to CRM / manual call
  Input: { name, email, company_domain }
        │
        ▼
┌──────────────────┐
│  STEP 1: MCP     │  company-enrichment-mcp
│  Enrich Lead     │  ───────────────────────────────────────────
│                  │  • Looks up company by domain
│  INPUT:          │  • Fetches from Apollo.io / Clearbit / LinkedIn
│  company_domain  │  • Finds recent signals:
│                  │    - New hires in last 90 days
│  OUTPUT:         │    - Job postings (signals of pain/growth)
│  enrichment{}    │    - Recent funding or product news
│                  │    - Tech stack (from BuiltWith)
│                  │    - Company size and revenue band
└────────┬─────────┘
         │
         │ enrichment{} JSON
         ▼
┌──────────────────┐
│  STEP 2: SKILL   │  personalised-outreach-drafter skill
│  Draft Email     │  ───────────────────────────────────────────
│                  │  • Picks best signal from enrichment data
│  INPUT:          │  • Maps signal → likely pain point
│  lead + enrich   │  • Writes email referencing that signal
│  data            │  • 3 subject line variants
│                  │  • Body: 4 lines max + CTA
│  OUTPUT:         │  • Tone: warm peer, not sales pitch
│  email_draft{}   │  • No open-ended questions at end
└────────┬─────────┘    • Specific, not generic
         │
         │ email_draft{} JSON
         ▼
┌──────────────────┐
│  STEP 3:         │  crm-connector
│  CONNECTOR       │  ───────────────────────────────────────────
│  Log to CRM      │  • Finds or creates contact in HubSpot
│                  │  • Saves email draft as a note
│  INPUT:          │  • Tags contact: "outreach-drafted"
│  email_draft{}   │  • Sets follow-up date (T+3 business days)
│                  │  • Optionally enqueues in email sequence
│  OUTPUT:         │  • Returns CRM contact URL
│  crm_result{}    │
└────────┬─────────┘
         │
         ▼
  [RESULT]
  Email draft saved to CRM ✓
  Contact tagged and follow-up scheduled
  Notify rep via Slack DM
```

---

## Step-by-Step Detail

### Step 1 — MCP: Enrich the Lead

**Server:** `company-enrichment-mcp`
**Tool called:** `enrich_company`

```json
// Input to MCP tool
{
  "domain": "acme.com",
  "contact_name": "John Smith",
  "contact_email": "john.smith@acme.com",
  "include": ["company_info", "tech_stack", "recent_news", "job_postings", "funding"]
}
```

```json
// Output from MCP tool
{
  "company": {
    "name": "Acme Corp",
    "domain": "acme.com",
    "industry": "B2B SaaS",
    "size": "51-200",
    "revenue_band": "$10M-$50M ARR",
    "location": "San Francisco, CA",
    "founded": 2018,
    "description": "Acme Corp builds workflow automation tools for mid-market operations teams."
  },
  "tech_stack": ["Salesforce", "HubSpot", "Zapier", "Slack", "Notion", "AWS"],
  "recent_signals": [
    {
      "type": "job_posting",
      "title": "Head of RevOps",
      "posted_days_ago": 14,
      "description": "Looking for someone to build out our revenue operations function from scratch. Must have experience with CRM data hygiene and sales process automation.",
      "signal_strength": "high"
    },
    {
      "type": "hiring",
      "title": "VP of Sales hired",
      "days_ago": 23,
      "detail": "Alex Rivera joined as VP of Sales from Outreach.io",
      "signal_strength": "high"
    },
    {
      "type": "news",
      "headline": "Acme Corp raises $12M Series A",
      "days_ago": 45,
      "url": "https://techcrunch.com/acme-series-a",
      "signal_strength": "medium"
    }
  ],
  "enriched_at": "2026-06-27T10:15:00Z"
}
```

---

### Step 2 — Skill: Draft the Outreach Email

**Skill:** `personalised-outreach-drafter`
**Input:** lead data + enrichment from Step 1

```json
// Output from skill
{
  "subject_lines": [
    "RevOps at Acme — one thing worth knowing",
    "The Head of RevOps hire → what usually comes next",
    "Quick thought on Acme's RevOps buildout"
  ],
  "email_body": "Hi John,\n\nSaw Acme is hiring a Head of RevOps — usually means CRM data hygiene and automation are about to become a priority.\n\nWe help ops teams at companies your size get their HubSpot data clean and their workflows running without manual work. Most see results in the first 2 weeks.\n\nWould it be worth a 15-minute call to see if it fits what you're building?\n\nBest,\n[Your name]",
  "signal_used": {
    "type": "job_posting",
    "detail": "Head of RevOps posting, 14 days ago"
  },
  "pain_point_mapped": "CRM data hygiene and sales process automation",
  "personalisation_score": 0.91,
  "email_word_count": 78,
  "follow_up_suggestion": "T+3 business days if no reply"
}
```

---

### Step 3 — Connector: Log to CRM

**Connector:** `crm-connector` (HubSpot)
**Action:** Create/update contact, add note, tag, set task

```json
// Output from connector
{
  "success": true,
  "crm": "hubspot",
  "contact_id": "32847291",
  "contact_url": "https://app.hubspot.com/contacts/8473621/contact/32847291",
  "actions_taken": [
    "Contact found: John Smith (existing)",
    "Note added: outreach email draft",
    "Tag applied: outreach-drafted",
    "Task created: Follow up on 2026-07-01",
    "Deal stage set: Prospecting"
  ],
  "logged_at": "2026-06-27T10:15:28Z"
}
```

---

## How to Trigger

### Option A — Single lead (CLI)
```bash
node run-workflow.js lead-workflow \
  --name "John Smith" \
  --email "john.smith@acme.com" \
  --domain "acme.com"
```

### Option B — Webhook (from CRM automation)
```bash
curl -X POST https://your-server.com/webhook/lead-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "contact": {
      "name": "John Smith",
      "email": "john.smith@acme.com",
      "domain": "acme.com"
    },
    "crm_contact_id": "32847291"
  }'
```

### Option C — Batch CSV
```bash
node run-workflow.js lead-workflow --batch leads.csv --concurrency 3
```

`leads.csv` format:
```
name,email,domain
John Smith,john.smith@acme.com,acme.com
Sarah Lee,sarah@widgetco.io,widgetco.io
```

---

## Successful Run Checklist

- [ ] MCP returns company data + at least 1 recent signal
- [ ] Skill produces email under 100 words with a specific signal referenced
- [ ] Skill personalisation_score >= 0.7
- [ ] CRM note created with email draft text
- [ ] Contact tagged "outreach-drafted"
- [ ] Follow-up task created in CRM
- [ ] Rep notified via Slack DM

See `sample_run.txt` for a complete real-output log.
