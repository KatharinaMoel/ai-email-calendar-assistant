# Week 2: Connect Nylas and Practice LLM Calls

## This Week's Goals

1. Connect an email account through Nylas hosted authentication
2. Read and send test emails through the Nylas API
3. Expose the local server with a Serveo tunnel
4. Register a webhook and receive your first new-email event
5. Practice the main types of LLM calls: a hosted generative model (OpenAI), structured output, a decision model (Jev), and an open source local model (Ollama)

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

## 6. Practice LLM Calls

The `week2/` folder has standalone quickstarts for each type of model call. See [week2/README.md](week2/README.md) for the dependencies, API keys, and run commands.

| File | What it shows |
|------|---------------|
| `week2/openai-quickstart.py` | Hosted generative model with an API key |
| `week2/structured_output.py` | Typed output with Pydantic and OpenAI |
| `week2/jev-quickstart.py` | Decision model with Choice, Score, and Noul |
| `week2/ollama-quickstart.py` | Open source model running locally, no key |
| `week2/pydantic-introduction.ipynb` | Pydantic basics |

## Troubleshooting

If the webhook stops working or returns errors, see the [Webhook Troubleshooting Guide](docs/webhook-troubleshoot-guide.md). It covers resetting an expired tunnel, `401` errors, firewall or VPN issues, and port conflicts.

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
