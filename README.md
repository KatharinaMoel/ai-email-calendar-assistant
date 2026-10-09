# Week 2: Connect Nylas

## This Week's Goals

1. Connect an email account through Nylas hosted authentication
2. Read and send test emails through the Nylas API
3. Expose the local server with a Serveo tunnel
4. Register a webhook and receive your first new-email event

## Before You Start

Complete the Week 1 homework first:

- `.env` contains `NYLAS_CLIENT_ID`, `NYLAS_API_KEY`, `NYLAS_API_URI`, and `EMAIL`
- The Nylas Dashboard lists `http://localhost:5010/oauth/exchange` as a callback URI

Install the dependencies:

```bash
uv sync
```

## 1. Connect Your Email Account

Start the authentication helper:

```bash
cd app/config
uv run config_auth.py
```

1. Visit `http://localhost:5010/nylas/auth` to begin authentication.
2. Log in with your email account and allow access.
3. Copy the returned grant ID into `.env`:

   ```env
   NYLAS_GRANT_ID=your_grant_id
   ```

4. Restart the helper so it loads the new value.
5. Visit `http://localhost:5010/nylas/recent-emails` to view your latest emails.
6. Visit `http://localhost:5010/nylas/send-email` to send a test email to your own account.

If `NYLAS_GRANT_ID` is already set, `/nylas/auth` returns that ID and skips the login. To connect a different account, clear the value first.

The flow looks like this:

```text
Browser → Nylas login → http://localhost:5010/oauth/exchange → grant ID
```

Nylas only redirects to callback URIs registered in the dashboard, which is why the Week 1 homework added it.

## 2. Configure a Tunnel

Nylas must reach your local server over the internet to deliver webhooks. We use [Serveo](https://serveo.net/), which needs no account or installation.

In a separate terminal, run:

```bash
ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -R 80:localhost:8000 serveo.net
```

Copy the public HTTPS URL it prints into `.env`:

```env
SERVER_URL=https://your-subdomain.serveo.net
```

Keep this terminal open. The URL usually changes each time you reconnect, so update `SERVER_URL` and register a new webhook when it does.

## 3. Start the Server

In another terminal:

```bash
cd app
uv run main.py
```

Visit `http://localhost:8000`. You should see the Nylas Webhooks page.

## 4. Create the Webhook

```bash
cd app/config
uv run config_webhook.py
```

This registers `SERVER_URL/events` with Nylas for new-email events and prints a webhook secret. Add it to `.env`:

```env
WEBHOOK_SECRET=your_webhook_secret
```

Restart `main.py` so it loads the secret. Then open **Notifications** in the Nylas Dashboard to confirm the webhook is listed.

When you register a new webhook for a new tunnel URL, delete the old one in the dashboard.

## 5. Test the Webhook

1. Send an email to the address in `EMAIL`.
2. Watch the `main.py` terminal for the incoming request and a `200` status.
3. Refresh `http://localhost:8000` to see the new message.

Each event is also saved as JSON in `requests/events/`. These files contain email content and are excluded from Git.

## Troubleshooting: Webhook Stops Working

The Nylas webhook becomes invalid once the tunnel URL expires or changes. To fix it:

1. Delete the webhook in the Nylas Dashboard under **Notifications**.
2. Clear `SERVER_URL` and `WEBHOOK_SECRET` in `.env`.
3. Run the Serveo SSH command and copy the new URL into `SERVER_URL`.
4. Start the server: `cd app` then `uv run main.py`.
5. In another terminal, create the webhook: `cd app/config` then `uv run config_webhook.py`.
6. Copy the printed secret into `WEBHOOK_SECRET`.
7. Stop the `main.py` server.
8. Start it again with `uv run main.py` so it loads the new secret.

## How the Pieces Fit

```text
config_webhook.py (run once)   tells Nylas where to send new-email events

New email → Nylas → Serveo tunnel → main.py /events → saved to requests/events/
                                                    → shown at localhost:8000
```

| File | Purpose |
|------|---------|
| `app/config/config_auth.py` | Hosted authentication and API checks on port 5010 |
| `app/config/config_webhook.py` | Registers the webhook with Nylas |
| `app/main.py` | Receives webhooks, verifies the signature, stores events |
| `app/schemas/nylas_webhook_schema.py` | Model for the webhook event wrapper |
| `app/schemas/nylas_email_schema.py` | Model for the email inside the event |
| `app/templates/index.html` | Page listing received emails |

`main.py` and the tunnel must both be running to receive emails.
