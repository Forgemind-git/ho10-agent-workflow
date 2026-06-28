# Connector: Email / Calendar Connector

> **Easiest path — use your Claude.ai subscription (no API key).** In Claude.ai, open **Settings → Connectors** and turn this integration on with one click — you sign in once and Claude can act on your behalf. For the course you do **not** need anything below.
>
> Everything that follows (OAuth apps, tokens, `.env` files, code) is the **optional, advanced** manual setup — only useful once you want the workflow to run unattended on a schedule.

## What This Connector Does

Delivers the morning brief via one or both of:
- **Email** — sends a formatted HTML email to yourself via Gmail API
- **Calendar event** — creates a 5-minute "Morning Brief" reading block at 07:00 in Google Calendar with the brief in the description

## Supported Delivery Methods

| Method | API | What it does |
|--------|-----|-------------|
| Gmail | Gmail API v1 | Sends HTML-formatted brief email to yourself |
| Google Calendar | Calendar API v3 | Creates a 5-min event with brief in description |
| Outlook / Microsoft 365 | Graph API | Alternative to Gmail for Microsoft-stack users |

---

## Gmail Setup

### Step 1 — Enable Gmail API

1. Go to https://console.cloud.google.com/
2. Create or select a project
3. Enable the **Gmail API** and **Google Calendar API**
4. Create **OAuth 2.0 credentials** (type: Desktop App)
5. Download `credentials.json`

### Step 2 — Authenticate (run once)

```python
# auth_setup.py — run this once to get your token.json
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar'
]

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

with open('token.json', 'w') as f:
    f.write(creds.to_json())

print("Authentication complete. token.json saved.")
```

### Step 3 — Send Email to Self

```python
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def send_morning_brief_email(brief_text: str, date_str: str, recipient: str) -> dict:
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('gmail', 'v1', credentials=creds)

    # Create HTML version of the brief
    html_body = brief_text.replace('\n', '<br>').replace('## ', '<h2>').replace('### ', '<h3>')

    message = MIMEMultipart('alternative')
    message['Subject'] = f'Morning Brief — {date_str}'
    message['To'] = recipient
    message['From'] = recipient

    # Attach both plain text and HTML
    part1 = MIMEText(brief_text, 'plain')
    part2 = MIMEText(html_body, 'html')
    message.attach(part1)
    message.attach(part2)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    result = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return {
        'method': 'email',
        'message_id': result['id'],
        'sent_at': datetime.utcnow().isoformat() + 'Z'
    }
```

---

## Google Calendar Setup

### Create a Morning Brief Event

```python
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_morning_brief_event(brief_text: str, date_str: str) -> dict:
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('calendar', 'v3', credentials=creds)

    # Set event for 07:00–07:05 on date_str
    start = datetime.strptime(f'{date_str}T07:00:00', '%Y-%m-%dT%H:%M:%S')
    end = start + timedelta(minutes=5)

    event = {
        'summary': f'Morning Brief — {start.strftime("%b %d")}',
        'description': brief_text,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'America/New_York'  # adjust to your timezone
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'America/New_York'
        },
        'reminders': {
            'useDefault': False,
            'overrides': []  # no reminder — it's a reading block
        },
        'colorId': '5'  # banana yellow — stands out in calendar
    }

    created = service.events().insert(calendarId='primary', body=event).execute()

    return {
        'method': 'calendar_event',
        'event_id': created['id'],
        'event_title': created['summary'],
        'event_start': created['start']['dateTime'],
        'calendar_url': created.get('htmlLink', '')
    }
```

---

## HTML Email Template

The connector formats the brief as a clean HTML email:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: -apple-system, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #1a1a1a; }
    h2 { color: #1a1a1a; border-bottom: 2px solid #f0f0f0; padding-bottom: 8px; }
    h3 { color: #333; margin-top: 24px; }
    .action-urgent { color: #dc2626; }
    .action-today { color: #d97706; }
    .focus { background: #f0f9ff; border-left: 3px solid #0284c7; padding: 12px 16px; margin: 16px 0; }
  </style>
</head>
<body>
  <!-- Brief content rendered from markdown -->
</body>
</html>
```

---

## Microsoft 365 Alternative

For Outlook users, use Microsoft Graph API:

```bash
# Send email via Graph API
curl -X POST https://graph.microsoft.com/v1.0/me/sendMail \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "subject": "Morning Brief — Jun 27",
      "body": {
        "contentType": "HTML",
        "content": "<h2>Morning Brief</h2>..."
      },
      "toRecipients": [{"emailAddress": {"address": "you@yourcompany.com"}}]
    }
  }'
```

---

## Environment Variables

```env
# Google OAuth
GOOGLE_CREDENTIALS_PATH=./credentials.json
GOOGLE_TOKEN_PATH=./token.json

# Delivery settings
BRIEFING_EMAIL_TO=you@yourcompany.com
BRIEFING_DELIVERY=both              # email | calendar | both
BRIEFING_CALENDAR_ID=primary
BRIEFING_CALENDAR_TIMEZONE=America/New_York
BRIEFING_CALENDAR_COLOR_ID=5        # banana yellow

# Microsoft 365 alternative
MS_TENANT_ID=your-tenant-id
MS_CLIENT_ID=your-client-id
MS_CLIENT_SECRET=your-client-secret
```

---

## Connector Output Schema

```json
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
      "calendar_url": "https://calendar.google.com/calendar/r/eventedit/evt_..."
    }
  ]
}
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid_grant` | OAuth token expired | Re-run `auth_setup.py` to refresh token |
| `quotaExceeded` | Gmail API quota (500 emails/day free) | This workflow sends 1/day — should never hit limit |
| `insufficientPermissions` | Missing OAuth scope | Re-auth with `gmail.send` + `calendar` scopes |
| Calendar event not appearing | Wrong calendar ID | Use `calendarList.list` to find correct ID |
