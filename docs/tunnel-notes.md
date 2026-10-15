# Tunnel Notes: Serveo and Alternatives

Week 2 uses [Serveo](https://serveo.net/) so Nylas can reach `main.py` on your laptop. That is fine for course exercises, but you should know what the tunnel exposes. Provider details below are from memory and not verified. Check each provider's documentation before you rely on them.

## What the tunnel exposes

- **The tunnel stays open while the `ssh` process runs.** It closes only with `Ctrl+C`, a closed terminal, sleep mode, or a dropped connection.
- **Only the forwarded port is public.** With `-R 80:localhost:8000` that is port 8000. The port is forwarded, not the program, so anything you later start on 8000 becomes public too.
- **All routes on that port are public.** `POST /events` checks the Nylas signature, but `GET /` shows received emails without a login.
- **Anyone with the URL gets in.** Serveo has no access control. A random subdomain is not a secret.
- **Serveo can read the traffic.** HTTPS ends on Serveo's servers, so webhook payloads pass through them unencrypted. This applies to every hosted tunnel, not just Serveo.

## Good habits

- Connect a test inbox rather than your personal email.
- Do not share the tunnel URL.
- Stop the tunnel and `main.py` when you are not testing.

## Alternatives for real projects

| Option | Notes |
|--------|-------|
| [ngrok](https://ngrok.com/) | Needs an account. Offers stable domains and optional login in front of the tunnel. |
| [Cloudflare Tunnel](https://developers.cloudflare.com/) (`cloudflared`) | Quick tunnels work without an account. Named tunnels give stable domains and optional Cloudflare Access login. |

Both are run by companies with published privacy terms and are more reliable than Serveo. Like Serveo, they terminate HTTPS on their side. A login in front of the tunnel does not work for webhooks, because Nylas cannot log in.
