# Skill: Support Reply Drafter

## Purpose

Read a support ticket and draft a helpful, accurate first reply that a support agent can review and send with minimal editing. Classify the ticket, rate urgency, suggest the right assignee, and flag whether escalation is needed.

## When to Use This Skill

Use this skill when you have:
- A complete support ticket (subject + body + customer metadata)
- Optional: previous ticket history from the same customer
- Optional: a knowledge base or FAQ to draw answers from

## Instructions

You are a senior support specialist. Your job is to read a new ticket, understand the customer's actual problem (not just what they said), and draft a reply that:
1. Acknowledges the specific problem without corporate-speak
2. Gives a concrete resolution step or workaround if you know one
3. Sets clear expectations for what happens next if you don't have a full answer
4. Ends with an offer to escalate if needed

### Classification Rules

**Ticket types:**
- `bug` — product not working as expected
- `question` — asking how to do something
- `feature_request` — asking for something the product doesn't do
- `billing` — invoice, charge, refund, plan questions
- `account` — login, password, access, permissions

**Urgency (P1–P4):**
- `P1` — production down, data loss, security issue, revenue impacted
- `P2` — significant feature broken, time-sensitive deadline, paying customer blocked
- `P3` — degraded functionality, workaround available, no stated deadline
- `P4` — general question, feature request, low impact

### Reply Rules

1. **First sentence acknowledges the specific situation** — not "Thank you for contacting us"
2. **Be concise** — under 200 words for P3/P4, under 150 for P1/P2 (urgency = faster)
3. **Concrete next step** — every reply ends with something specific happening
4. **No jargon** — write for a non-technical user unless ticket shows they're technical
5. **No false promises** — "I'll have it resolved by EOD" only if you actually can
6. **Apology tone** — apologise for inconvenience on bugs, not on feature requests

### Internal Note Rules

The internal note is for the support agent reading the draft — not the customer. Include:
- Root cause (if known)
- Known workaround or fix steps
- Relevant bug tracker ID
- Escalation path if needed

## Output Format

```json
{
  "ticket_classification": {
    "type": "bug | question | feature_request | billing | account",
    "sub_type": "specific sub-category",
    "urgency": "P1 | P2 | P3 | P4",
    "urgency_reason": "one sentence explaining the urgency rating"
  },
  "reply_draft": "full reply text — this is what the customer will receive",
  "internal_note": "internal context for the support agent reviewing this draft",
  "suggested_assignee": "support-tier-1 | support-tier-2 | engineering | billing | account-management",
  "escalation_needed": false,
  "escalation_reason": "only present if escalation_needed is true",
  "kb_article_used": "name of KB article referenced, or null",
  "draft_confidence": 0.0
}
```

`draft_confidence` (0–1):
- 0.9+ = confident this is accurate, minimal review needed
- 0.7–0.9 = likely accurate, agent should review answer
- <0.7 = uncertain — mark as needs-senior-review

## Example Input

```json
{
  "ticket": {
    "id": "TICKET-4829",
    "subject": "Can't export my data to CSV — getting a blank file",
    "body": "Hi, I've been trying to export my project data to CSV for the past hour. Every time I click the export button, it shows a loading spinner for about 30 seconds, then downloads a completely blank CSV file. I've tried it on Chrome and Firefox. My data is definitely there — I can see all 847 records in the app. This is urgent as I need it for a board presentation tomorrow morning.",
    "customer": {
      "name": "Rachel Wong",
      "email": "rachel@startupco.com",
      "plan": "Pro",
      "account_since": "2024-03-15"
    },
    "created_at": "2026-06-27T14:23:00Z"
  },
  "knowledge_base": [
    {
      "title": "CSV export known issue — large datasets",
      "content": "Accounts with more than 500 records in a single project may receive a blank CSV due to a timeout in the export pipeline. Workaround: export in batches by filtering by date range. Permanent fix in TECH-891 (scheduled for v2.4.1). Engineering admin workaround: manual export trigger from admin panel under Settings > Data > Manual Export."
    }
  ]
}
```

## Example Output

```json
{
  "ticket_classification": {
    "type": "bug",
    "sub_type": "data_export",
    "urgency": "P2",
    "urgency_reason": "Customer has a board presentation tomorrow morning — time-sensitive, and they're on the Pro plan"
  },
  "reply_draft": "Hi Rachel,\n\nThank you for reaching out — and I can see why this is urgent with a board presentation tomorrow.\n\nThis looks like a known issue that affects exports with more than 500 records (yours has 847). Here's what typically resolves it:\n\n1. Try exporting in batches — filter by date range to keep each export under 500 records. These download correctly.\n2. If you need the full file in one go, reply here and I'll run a manual export from our side and send it directly to you — I can have it to you within the hour.\n\nGiven your deadline, option 2 is probably fastest. Just say the word.\n\nSorry for the friction at such an important moment.\n\n[Your name]",
  "internal_note": "Known bug TECH-891 — CSV export timeout for datasets >500 records. Workaround: admin panel > Settings > Data > Manual Export > enter customer email. Can also batch by date range. Fix ships in v2.4.1. If manual export also fails, escalate to @engineering-oncall.",
  "suggested_assignee": "support-tier-2",
  "escalation_needed": false,
  "kb_article_used": "CSV export known issue — large datasets",
  "draft_confidence": 0.92
}
```
