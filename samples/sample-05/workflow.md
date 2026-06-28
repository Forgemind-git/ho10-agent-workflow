# Workflow: Personal Morning Briefing

## Overview

This workflow runs at 06:45 every weekday morning. It gathers your calendar, emails, and news, then delivers a concise briefing — so the first thing you do each morning is read a one-page summary, not triage 40 inboxes.

**Trigger options:**
- Scheduled: cron at 06:45 Monday–Friday
- Manual: `node run-workflow.js morning-briefing --date today`
- On-demand: call via CLI any time for an instant briefing

**Duration:** ~30–45 seconds end-to-end

---

## ASCII Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                  PERSONAL MORNING BRIEFING                      │
└─────────────────────────────────────────────────────────────────┘

  [TRIGGER]
  Cron 06:45 Mon–Fri
        │
        ▼
┌──────────────────┐
│  STEP 1: MCP     │  morning-inputs-mcp
│  Gather Inputs   │  ───────────────────────────────────────────
│                  │  • Google Calendar: today's events
│  INPUT:          │  • Gmail: top 10 unread emails
│  date = today    │    (sorted by importance heuristic)
│                  │  • News RSS: 5 relevant headlines
│  OUTPUT:         │  • Weather (optional)
│  inputs{}        │  Returns all in a single structured object
└────────┬─────────┘
         │
         │ inputs{} JSON
         ▼
┌──────────────────┐
│  STEP 2: SKILL   │  morning-brief-summariser skill
│  Write Brief     │  ───────────────────────────────────────────
│                  │  • Identifies today's most important meeting
│  INPUT:          │  • Flags emails needing action today
│  inputs{}        │  • Surfaces the 1 most relevant news item
│  + user prefs    │  • Sets a single "focus of the day"
│                  │  • Writes under 300 words total
│  OUTPUT:         │  • Structured sections: Schedule / Email /
│  brief{}         │    News / Focus
└────────┬─────────┘
         │
         │ brief{} JSON
         ▼
┌──────────────────┐
│  STEP 3:         │  email-calendar-connector
│  CONNECTOR       │  ───────────────────────────────────────────
│  Deliver Brief   │  OPTION A — Email delivery:
│                  │  • Gmail API → send to self
│  INPUT:          │  • Subject: "Morning Brief — Mon Jun 27"
│  brief{}         │  • HTML formatted email
│                  │
│  OUTPUT:         │  OPTION B — Calendar event:
│  delivery{}      │  • Create "☀️ Morning Brief" event at 07:00
│                  │  • Duration: 5 minutes (reading time)
│                  │  • Brief text in event description
└────────┬─────────┘
         │
         ▼
  [RESULT]
  Brief delivered ✓
  Ready to read before 07:00
```

---

## Step-by-Step Detail

### Step 1 — MCP: Gather Morning Inputs

**Server:** `morning-inputs-mcp`
**Tool called:** `get_morning_inputs`

```json
// Input to MCP tool
{
  "date": "2026-06-27",
  "gmail_max_emails": 10,
  "gmail_label_filter": "INBOX",
  "calendar_hours_ahead": 24,
  "news_topics": ["artificial intelligence", "business", "tech"],
  "news_max_items": 5
}
```

```json
// Output from MCP tool
{
  "date": "2026-06-27",
  "day_of_week": "Friday",
  "calendar": {
    "events": [
      {
        "title": "Weekly team standup",
        "start": "2026-06-27T09:00:00",
        "end": "2026-06-27T09:30:00",
        "attendees": ["alice@co.com", "bob@co.com", "carol@co.com"],
        "meeting_link": "https://meet.google.com/xyz-abc-def"
      },
      {
        "title": "1:1 with Alex (VP Sales)",
        "start": "2026-06-27T11:00:00",
        "end": "2026-06-27T11:30:00",
        "attendees": ["alex@co.com"],
        "notes": "Q2 pipeline review — come prepared with updated forecast"
      },
      {
        "title": "Product demo — Acme Corp",
        "start": "2026-06-27T14:00:00",
        "end": "2026-06-27T15:00:00",
        "attendees": ["john.smith@acme.com", "sarah.jones@acme.com"],
        "notes": "Enterprise demo. Acme is evaluating us vs Competitor X."
      }
    ],
    "total_events": 3,
    "free_blocks": [
      { "start": "09:30", "end": "11:00", "duration_minutes": 90 },
      { "start": "11:30", "end": "14:00", "duration_minutes": 150 }
    ]
  },
  "emails": {
    "unread_count": 23,
    "top_emails": [
      {
        "from": "alex@co.com",
        "subject": "Q2 forecast — need your numbers by 10am",
        "preview": "Hey, can you update the shared sheet with your team's Q2 actuals before our 11am 1:1? I need...",
        "received_at": "2026-06-26T22:47:00Z",
        "importance": "high",
        "requires_action": true,
        "action_deadline": "10:00"
      },
      {
        "from": "noreply@stripe.com",
        "subject": "Your June invoice is ready",
        "preview": "Your invoice for $2,847.00 is ready to view.",
        "received_at": "2026-06-27T00:00:00Z",
        "importance": "medium",
        "requires_action": false
      },
      {
        "from": "john.smith@acme.com",
        "subject": "Re: Tomorrow's demo — one question",
        "preview": "Hi, just wanted to confirm — will you be showing the API integration flow during the demo? We have a...",
        "received_at": "2026-06-26T19:03:00Z",
        "importance": "high",
        "requires_action": true,
        "action_deadline": "before 14:00"
      }
    ]
  },
  "news": [
    {
      "headline": "OpenAI announces enterprise pricing overhaul",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/...",
      "summary": "New per-seat model replaces token-based pricing for enterprise customers.",
      "relevance_score": 0.89
    },
    {
      "headline": "EU AI Act compliance deadline extended by 6 months",
      "source": "Reuters",
      "url": "https://reuters.com/...",
      "summary": "High-risk AI systems now have until December 2026 to comply.",
      "relevance_score": 0.72
    }
  ],
  "fetched_at": "2026-06-27T06:45:08Z"
}
```

---

### Step 2 — Skill: Write the Morning Brief

**Skill:** `morning-brief-summariser`

```json
// Output from skill
{
  "date": "2026-06-27",
  "brief_text": "## Morning Brief — Friday, June 27\n\n### Today's Schedule\n3 meetings | Heaviest block: 14:00 demo with Acme Corp\n\n09:00 — Team standup (30 min)\n11:00 — 1:1 with Alex: Q2 pipeline review\n14:00 — Acme Corp demo (1 hour) — enterprise evaluation vs Competitor X\n\nBiggest free block: 11:30–14:00 (2.5 hours) — use it for deep work\n\n### Emails Needing Action\n🔴 From Alex (10am deadline): Update Q2 actuals in shared sheet before your 11am 1:1.\n🟡 From John Smith / Acme: Confirm whether you'll demo the API integration today. Reply before 14:00.\n\n### News Worth Knowing\nOpenAI is changing enterprise pricing to per-seat. If Acme asks about AI tool costs during your demo today, this context is relevant.\n\n### Focus of the Day\nThe Acme demo is the most consequential thing today. Block 30 minutes before 14:00 to prep the API integration flow (John's email suggests they'll ask about it). Everything else can wait until after.",
  "actions_needed": [
    {
      "action": "Update Q2 actuals in shared sheet",
      "deadline": "10:00",
      "source": "Email from Alex"
    },
    {
      "action": "Reply to John Smith: confirm API demo",
      "deadline": "before 14:00",
      "source": "Email from john.smith@acme.com"
    }
  ],
  "focus_of_day": "Acme Corp demo prep — especially the API integration flow",
  "word_count": 198,
  "generated_at": "2026-06-27T06:45:21Z"
}
```

---

### Step 3 — Connector: Deliver the Brief

**Connector:** `email-calendar-connector`
**Action:** Send email to self + create calendar event

```json
// Output from connector
{
  "success": true,
  "delivery_methods": [
    {
      "method": "email",
      "recipient": "you@yourcompany.com",
      "message_id": "msg_18b4f2e9a3c1d457",
      "sent_at": "2026-06-27T06:45:35Z"
    },
    {
      "method": "calendar_event",
      "event_id": "evt_9f2c8a1b7d4e3f56",
      "event_title": "Morning Brief — Jun 27",
      "event_start": "2026-06-27T07:00:00",
      "calendar_url": "https://calendar.google.com/calendar/r/eventedit/evt_9f2c8a1b7d4e3f56"
    }
  ]
}
```

---

## How to Trigger

### Option A — Cron (recommended)
```bash
# Run at 06:45 Mon–Fri
45 6 * * 1-5 cd /your/project && node run-workflow.js morning-briefing
```

### Option B — Manual (instant briefing anytime)
```bash
node run-workflow.js morning-briefing --date today --delivery email
```

### Option C — Different delivery
```bash
# Calendar only
node run-workflow.js morning-briefing --delivery calendar

# Email only
node run-workflow.js morning-briefing --delivery email

# Both (default)
node run-workflow.js morning-briefing --delivery both
```

---

## Personalisation Options

Set in your `.env` or config:

```env
# Focus areas for news filtering
NEWS_TOPICS=artificial intelligence,business strategy,your industry

# Delivery preference
BRIEFING_DELIVERY=both         # email | calendar | both

# Email recipient (usually yourself)
BRIEFING_EMAIL_TO=you@yourcompany.com

# Calendar to add event to
BRIEFING_CALENDAR_ID=primary

# Max brief length (words)
BRIEFING_MAX_WORDS=300
```

---

## Successful Run Checklist

- [ ] MCP returns calendar events for today
- [ ] MCP returns at least 5 unread emails
- [ ] Skill brief is under 300 words
- [ ] At least 1 action item identified
- [ ] Email delivered successfully (check message_id)
- [ ] Calendar event created at 07:00

See `sample_run.txt` for a complete real-output log.
