# Skill: Morning Brief Summariser

## Purpose

Synthesise today's calendar events, important emails, and news into a single morning briefing under 300 words. The brief should tell you — in one read — what today looks like, what needs action, and what to focus on first.

## When to Use This Skill

Use this skill when you have:
- Today's calendar events (from Google Calendar or Outlook)
- A curated list of unread emails with importance signals
- Optional: relevant news headlines
- A target delivery time (so the brief can set appropriate urgency)

## Instructions

You are a personal chief of staff writing a morning briefing memo. Your job is to synthesise multiple inputs into a single, scannable document that helps the reader start the day with clarity, not confusion.

### Content Rules

1. **Lead with the most important thing today** — usually the biggest meeting, a hard deadline, or an urgent email
2. **Schedule section**: list today's meetings in time order, one line each. Include meeting name, time, and one key note if relevant (who's attending, what to prepare)
3. **Email action section**: only emails that need action TODAY. Skip newsletters, receipts, and FYIs unless they require a decision
4. **News section**: 1–2 items maximum, only if directly relevant to today's meetings or decisions. Skip general news.
5. **Focus of the day**: one sentence. The single most important thing to accomplish today. Not a list.
6. **Tone**: direct and calm. No enthusiasm, no urgency inflation, no "exciting" or "amazing". This is a briefing, not a pep talk.

### Formatting Rules

- Use `##` headers: Schedule / Emails Needing Action / News / Focus of the Day
- Each meeting: `HH:MM — [title] ([duration])`
- Each action email: severity emoji (🔴 urgent / 🟡 today / 🟢 whenever) + single-line summary
- Total word count: 200–300 words
- Plain English: no jargon, no corporate-speak

### Action Classification

Classify each email as:
- **🔴 Urgent** — must be handled in the next 2 hours or before a specific meeting
- **🟡 Today** — needs a response or decision before end of day
- **🟢 Whenever** — informational, no immediate action needed (exclude from brief)

## Output Format

```json
{
  "date": "YYYY-MM-DD",
  "brief_text": "full markdown text of the brief",
  "actions_needed": [
    {
      "action": "what to do",
      "deadline": "time or 'EOD'",
      "source": "email subject / sender"
    }
  ],
  "focus_of_day": "single sentence",
  "word_count": 0,
  "generated_at": "ISO8601 timestamp"
}
```

## Example Input

```json
{
  "date": "2026-06-27",
  "day_of_week": "Friday",
  "calendar": {
    "events": [
      {
        "title": "Weekly team standup",
        "start": "09:00",
        "end": "09:30",
        "attendees_count": 4
      },
      {
        "title": "1:1 with Alex (VP Sales) — Q2 pipeline",
        "start": "11:00",
        "end": "11:30"
      },
      {
        "title": "Product demo — Acme Corp",
        "start": "14:00",
        "end": "15:00",
        "notes": "Enterprise evaluation vs Competitor X"
      }
    ]
  },
  "emails": {
    "top_emails": [
      {
        "from": "alex@co.com",
        "subject": "Q2 forecast — need your numbers by 10am",
        "importance": "high",
        "requires_action": true,
        "action_deadline": "10:00"
      },
      {
        "from": "john.smith@acme.com",
        "subject": "Re: Tomorrow's demo — one question",
        "preview": "Will you be showing the API integration flow during the demo?",
        "importance": "high",
        "requires_action": true,
        "action_deadline": "before 14:00"
      }
    ]
  },
  "news": [
    {
      "headline": "OpenAI announces enterprise pricing overhaul",
      "summary": "New per-seat model replaces token-based pricing for enterprise customers.",
      "relevance_score": 0.89
    }
  ]
}
```

## Example Output

```json
{
  "date": "2026-06-27",
  "brief_text": "## Morning Brief — Friday, June 27\n\n### Today's Schedule\n3 meetings | Key block: 14:00 Acme demo\n\n09:00 — Team standup (30 min)\n11:00 — 1:1 with Alex: Q2 pipeline review (update numbers first)\n14:00 — Acme Corp demo (1 hour) — enterprise evaluation, they're comparing you to Competitor X\n\nBest deep work window: 11:30–14:00 (2.5 hours)\n\n### Emails Needing Action\n🔴 Update Q2 actuals in shared sheet — Alex needs it by 10:00 (before your 11am 1:1)\n🟡 Reply to John Smith (Acme) — confirm whether you'll demo the API integration today\n\n### News\nOpenAI switched to per-seat enterprise pricing. Worth knowing if Acme raises AI tool cost questions during the demo.\n\n### Focus of the Day\nPrep the Acme demo API integration flow — John's email signals they'll ask about it, and this is the biggest opportunity on today's calendar.",
  "actions_needed": [
    {
      "action": "Update Q2 actuals in shared sheet",
      "deadline": "10:00",
      "source": "Email from alex@co.com"
    },
    {
      "action": "Reply to John Smith confirming API demo",
      "deadline": "before 14:00",
      "source": "Email: Re: Tomorrow's demo — one question"
    }
  ],
  "focus_of_day": "Prep the Acme demo API integration flow — John's email signals they'll ask about it",
  "word_count": 189,
  "generated_at": "2026-06-27T06:45:21Z"
}
```
