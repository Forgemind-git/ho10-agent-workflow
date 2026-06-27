# Connector: CRM (HubSpot / Notion) Connector

## What This Connector Does

After the Personalised Outreach Drafter skill produces an email draft, this connector:
1. Finds or creates the contact in HubSpot (or Notion CRM)
2. Saves the email draft as a note on the contact
3. Tags the contact with `outreach-drafted`
4. Creates a follow-up task for the assigned rep
5. Optionally enqueues the email in a HubSpot sequence

## Supported CRMs

| CRM | Method | Complexity |
|-----|--------|-----------|
| HubSpot | REST API v3 | Low — well-documented, free tier available |
| Notion | Notion API v1 | Medium — requires database setup |
| Airtable | Airtable API | Low — good for small teams |

---

## HubSpot Setup

### Step 1 — Create a Private App

1. Go to your HubSpot account → Settings → Integrations → Private Apps
2. Click **Create a private app**
3. Name it: "Lead Outreach Workflow"
4. Under **Scopes**, enable:
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`
   - `crm.objects.notes.write`
   - `crm.objects.tasks.write`
   - `crm.lists.write`
5. Click **Create app** and copy the **Access Token**

### Step 2 — Find or Create a Contact

```bash
# Search for existing contact by email
curl -X POST https://api.hubapi.com/crm/v3/objects/contacts/search \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filterGroups": [{
      "filters": [{
        "propertyName": "email",
        "operator": "EQ",
        "value": "john.smith@acme.com"
      }]
    }],
    "properties": ["email", "firstname", "lastname", "company"]
  }'
```

```bash
# Create contact if not found
curl -X POST https://api.hubapi.com/crm/v3/objects/contacts \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "email": "john.smith@acme.com",
      "firstname": "John",
      "lastname": "Smith",
      "company": "Acme Corp",
      "lifecyclestage": "lead",
      "hs_lead_status": "NEW"
    }
  }'
```

### Step 3 — Add a Note with the Email Draft

```bash
curl -X POST https://api.hubapi.com/crm/v3/objects/notes \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "hs_note_body": "OUTREACH DRAFT\n\nSubject: RevOps at Acme — one thing worth knowing\n\n[Email body here]",
      "hs_timestamp": "2026-06-27T10:15:28Z"
    },
    "associations": [{
      "to": { "id": "CONTACT_ID" },
      "types": [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 202
      }]
    }]
  }'
```

### Step 4 — Create a Follow-Up Task

```bash
curl -X POST https://api.hubapi.com/crm/v3/objects/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "hs_task_subject": "Follow up with John Smith (Acme Corp)",
      "hs_task_body": "Send outreach email. Draft in contact notes.",
      "hs_task_status": "NOT_STARTED",
      "hs_task_type": "EMAIL",
      "hs_timestamp": "2026-07-01T09:00:00Z",
      "hubspot_owner_id": "YOUR_OWNER_ID"
    },
    "associations": [{
      "to": { "id": "CONTACT_ID" },
      "types": [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216
      }]
    }]
  }'
```

---

## Notion CRM Setup (Alternative)

### Step 1 — Set Up Notion Integration

1. Go to https://www.notion.so/my-integrations → New Integration
2. Name it "Lead Outreach Workflow"
3. Select the workspace
4. Copy the **Internal Integration Token**
5. Share your CRM database with the integration (open database → Share → Add integration)

### Step 2 — Find Your Database ID

The database ID is in the URL: `https://notion.so/YOUR_DATABASE_ID?v=...`

### Step 3 — Create a Contact Record

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer YOUR_INTEGRATION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": { "database_id": "YOUR_DATABASE_ID" },
    "properties": {
      "Name": { "title": [{ "text": { "content": "John Smith" } }] },
      "Email": { "email": "john.smith@acme.com" },
      "Company": { "rich_text": [{ "text": { "content": "Acme Corp" } }] },
      "Status": { "select": { "name": "outreach-drafted" } },
      "Follow Up Date": { "date": { "start": "2026-07-01" } }
    },
    "children": [{
      "object": "block",
      "type": "callout",
      "callout": {
        "rich_text": [{ "text": { "content": "OUTREACH DRAFT\n\n[Subject + body here]" } }],
        "icon": { "emoji": "✉️" }
      }
    }]
  }'
```

---

## Environment Variables

```env
# HubSpot
HUBSPOT_ACCESS_TOKEN=pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
HUBSPOT_OWNER_ID=12345678
HUBSPOT_PORTAL_ID=8473621

# Notion (if using Notion)
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxx
NOTION_CRM_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Workflow settings
CRM_PROVIDER=hubspot
FOLLOWUP_DAYS=3
NOTIFY_REP_SLACK=true
```

---

## Connector Output Schema

```json
{
  "success": true,
  "crm": "hubspot",
  "contact_id": "32847291",
  "contact_url": "https://app.hubspot.com/contacts/8473621/contact/32847291",
  "actions_taken": [
    "Contact found: John Smith (existing)",
    "Note added: outreach email draft (note_id: 47829301)",
    "Tag applied: outreach-drafted",
    "Task created: Follow up on 2026-07-01 (task_id: 91827364)",
    "Deal stage set: Prospecting"
  ],
  "logged_at": "2026-06-27T10:15:28Z"
}
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or expired access token | Regenerate Private App token |
| 404 Contact not found | Contact ID mismatch | Re-search by email before associating |
| 429 Rate Limited | Too many API calls | Add delay between batch leads; HubSpot free: 100 req/10s |
| 400 Bad Request | Missing required property | Check schema — `hs_task_subject` is required for tasks |
