# Email Capture Files

These are the files used in Part 1 of the Week 2 README, which captures new emails on your laptop.

| File | Purpose |
|------|---------|
| `app/config/config_auth.py` | Hosted authentication and API checks on port 5010 |
| `app/config/config_webhook.py` | Registers the webhook with Nylas (run once per tunnel URL) |
| `app/main.py` | Receives webhooks, verifies the signature, stores events |
| `app/schemas/nylas_webhook_schema.py` | Model for the webhook event wrapper |
| `app/schemas/nylas_email_schema.py` | Model for the email inside the event |
| `app/templates/index.html` | Page listing received emails |
