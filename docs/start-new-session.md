# Start a New Session

Some Part 1 steps in the Week 2 README run once, and some run every time you work on the project:

| Step | When to run it |
|------|----------------|
| Step 1: Connect your email account | Once. Run it again only to switch accounts or if your grant expires. |
| Step 2: Start the tunnel | Every session, and again whenever it drops |
| Step 3: Start `main.py` | Every session |
| Step 4: Create the webhook | Only when the tunnel URL changes |
| Step 5: Test the webhook | Whenever you want to confirm emails are arriving |

If you finished Part 1 before and are coming back to test again:

1. Start the tunnel: `ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -R 80:localhost:8000 serveo.net`
2. Start the server: `cd app` then `uv run main.py`
3. Compare the tunnel URL with `SERVER_URL` in `.env`.
   - **Same URL:** You're done. Send yourself an email to test.
   - **Different URL:** Delete the old webhook under **Notifications** in the Nylas Dashboard, update `SERVER_URL`, then continue below.
4. Run `cd app/config` then `uv run config_webhook.py` to create the webhook and get a new secret.
5. Paste the secret into `WEBHOOK_SECRET` in `.env`.
6. **Restart `main.py` so it loads the new secret.**
7. Send yourself an email to test.

If it still doesn't work, see the [Webhook Troubleshooting Guide](webhook-troubleshoot-guide.md).
