# Workflow: Support Ticket Workflow

## Overview

This workflow intercepts new support tickets, drafts a first reply in under 20 seconds, and saves it as an internal note for human review. The human reviews and clicks send — they never write from scratch again.

**Trigger options:**
- Webhook: triggered by new ticket webhook from Intercom/Zendesk
- Polling: check for new tickets every 2 minutes
- Manual: `node run-workflow.js support-workflow --ticket-id TICKET-123`

**Duration:** ~15–25 seconds per ticket

---

## ASCII Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPPORT TICKET WORKFLOW                      │
└─────────────────────────────────────────────────────────────────┘

  [TRIGGER]
  New ticket arrives (webhook or poll)
        │
        ▼
┌──────────────────┐
│  STEP 1: MCP     │  support-ticket-mcp
│  Fetch Ticket    │  ───────────────────────────────────────────
│                  │  • Fetches ticket by ID or latest unhandled
│  INPUT:          │  • Returns: subject, body, customer info,
│  ticket_id or    │    attachment list, previous messages
│  "latest"        │  • Also fetches related tickets from same
│                  │    customer (for context)
│  OUTPUT:         │  • Looks up customer plan/tier from CRM
│  ticket{}        │
└────────┬─────────┘
         │
         │ ticket{} JSON
         ▼
┌──────────────────┐
│  STEP 2: SKILL   │  support-reply-drafter skill
│  Draft Reply     │  ───────────────────────────────────────────
│                  │  • Classifies ticket type (bug / question /
│  INPUT:          │    feature request / billing / account)
│  ticket{}        │  • Rates urgency (P1–P4)
│                  │  • Checks knowledge base (if configured)
│  OUTPUT:         │  • Drafts reply in support voice
│  reply_draft{}   │  • Flags if escalation is needed
│                  │  • Suggests assignee
└────────┬─────────┘
         │
         │ reply_draft{} JSON
         ▼
┌──────────────────┐
│  STEP 3:         │  ticket-tracker-connector
│  CONNECTOR       │  ───────────────────────────────────────────
│  Update Ticket   │  • Adds draft reply as internal note
│                  │  • Updates status: "reply-drafted"
│  INPUT:          │  • Assigns to suggested team member
│  reply_draft{}   │  • Sets priority based on urgency rating
│                  │  • Returns ticket URL
│  OUTPUT:         │
│  update_result{} │
└────────┬─────────┘
         │
         ▼
  [RESULT]
  Internal note added ✓
  Ticket status updated
  Assignee notified via Slack/email
  Human reviews draft and clicks send
```

---

## Step-by-Step Detail

### Step 1 — MCP: Fetch the Ticket

**Server:** `support-ticket-mcp`
**Tool called:** `get_ticket`

```json
// Input to MCP tool
{
  "ticket_id": "TICKET-4829",
  "include": ["customer_history", "attachments", "customer_plan"]
}
```

```json
// Output from MCP tool
{
  "ticket": {
    "id": "TICKET-4829",
    "subject": "Can't export my data to CSV — getting a blank file",
    "body": "Hi, I've been trying to export my project data to CSV for the past hour. Every time I click the export button, it shows a loading spinner for about 30 seconds, then downloads a completely blank CSV file. I've tried it on Chrome and Firefox. My data is definitely there — I can see all 847 records in the app. This is urgent as I need it for a board presentation tomorrow morning. Thanks",
    "customer": {
      "name": "Rachel Wong",
      "email": "rachel@startupco.com",
      "plan": "Pro",
      "account_since": "2024-03-15",
      "ticket_history_count": 3
    },
    "created_at": "2026-06-27T14:23:00Z",
    "status": "open",
    "attachments": [],
    "previous_tickets": [
      {
        "id": "TICKET-3201",
        "subject": "Login issue resolved",
        "status": "closed",
        "days_ago": 45
      }
    ]
  },
  "fetched_at": "2026-06-27T14:23:05Z"
}
```

---

### Step 2 — Skill: Draft the Reply

**Skill:** `support-reply-drafter`

```json
// Output from skill
{
  "ticket_classification": {
    "type": "bug",
    "sub_type": "data_export",
    "urgency": "P2",
    "urgency_reason": "Customer has a board presentation tomorrow morning — time-sensitive"
  },
  "reply_draft": "Hi Rachel,\n\nThank you for reaching out — and I can see why this is urgent with a board presentation tomorrow.\n\nThis sounds like our CSV export issue that affects accounts with more than 500 records in a single project. Here's what typically resolves it:\n\n1. Try exporting a filtered subset first (e.g. filter by date range to get batches under 500 records) — these usually download correctly\n2. If the full export is essential, reply here and I'll trigger a manual export from our side and send you the file directly\n\nGiven your timeline, I'd recommend replying immediately if you need the full file — I can have it to you within the hour.\n\nSorry for the friction at such an important moment.\n\n[Your name]",
  "internal_note": "Known issue: CSV export times out for >500 records. Workaround: manual export trigger from admin panel (Settings > Data > Manual Export > enter customer email). Can also batch-export by date range. Escalate to engineering if workaround fails. Bug tracked in TECH-891.",
  "suggested_assignee": "support-tier-2",
  "escalation_needed": false,
  "kb_article_used": "CSV export known issue — large datasets",
  "draft_confidence": 0.92
}
```

---

### Step 3 — Connector: Update the Ticket

**Connector:** `ticket-tracker-connector` (Linear)

```json
// Output from connector
{
  "success": true,
  "tracker": "linear",
  "ticket_id": "TICKET-4829",
  "ticket_url": "https://linear.app/yourteam/issue/TICKET-4829",
  "actions_taken": [
    "Status updated: open → reply-drafted",
    "Priority set: P2",
    "Internal note added: draft reply (380 chars)",
    "Internal note added: internal context for agent",
    "Assigned to: support-tier-2 (@alex_support)",
    "Label added: bug, data-export"
  ],
  "updated_at": "2026-06-27T14:23:22Z"
}
```

---

## How to Trigger

### Option A — Webhook (recommended for real-time)
Configure your support platform to send a webhook on new ticket creation:

```bash
# Intercom webhook example
curl -X POST https://your-server.com/webhook/support-workflow \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": "TICKET-4829", "source": "intercom"}'
```

### Option B — Polling (if webhooks aren't available)
```bash
# Run every 2 minutes via cron
*/2 * * * * node run-workflow.js support-workflow --mode poll --status new
```

### Option C — Manual (for testing or backlog)
```bash
node run-workflow.js support-workflow --ticket-id TICKET-4829
```

---

## Human-in-the-Loop Design

This workflow deliberately keeps a human in the loop:

1. **Draft is internal note only** — never sent automatically
2. **Agent reviews and clicks "Send"** — takes 10 seconds instead of 10 minutes
3. **Escalation flag** — skill flags tickets needing senior review
4. **Confidence score** — low confidence (<0.7) triggers a "needs review" label

This design means the workflow speeds up your team without risking an automated wrong answer going to a customer.

---

## Successful Run Checklist

- [ ] MCP returns full ticket with customer context
- [ ] Skill classifies ticket type and urgency
- [ ] Reply draft is under 250 words
- [ ] Internal note added to ticket
- [ ] Status updated to "reply-drafted"
- [ ] Assignee set based on ticket type
- [ ] Support rep notified

See `sample_run.txt` for a complete real-output log.
