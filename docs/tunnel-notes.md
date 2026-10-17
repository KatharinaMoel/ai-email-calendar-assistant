# Tunnel Notes: Serveo and Alternatives

Week 2 used [Serveo](https://serveo.net/) so Nylas can reach `main.py` on your laptop; since Week 3 this fork uses a Cloudflare Quick Tunnel instead (Serveo dropped too often, see below). Either way, you should know what the tunnel exposes. Provider details below are from memory and not verified. Check each provider's documentation before you rely on them.

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
| [ngrok](https://ngrok.com/) | **Does not work with Nylas.** The [Nylas v3 webhook docs](https://developer.nylas.com/docs/v3/notifications/webhooks/) (checked 2026-10-17): “Nylas blocks requests to Ngrok testing URLs because of throughput limiting concerns.” |
| [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-local-tunnel) (`cloudflared`) | Quick tunnels work without an account; the URL changes on every restart. Named tunnels give stable domains (needs a Cloudflare account and your own domain) and optional Cloudflare Access login. Nylas itself offers `cloudflared` as a tunnel for its CLI. |

Cloudflare is run by a company with published privacy terms and is more reliable than Serveo. Like Serveo, it terminates HTTPS on its side. A login in front of the tunnel does not work for webhooks, because Nylas cannot log in.

## Cloudflare Quick Tunnel (used since Week 3)

**Install once (Fedora, dnf5)** from Cloudflare's package repository, so `dnf upgrade` keeps it current:

```bash
# official file per pkg.cloudflare.com; there the dnf4 syntax: dnf config-manager --add-repo <url>
sudo dnf config-manager addrepo --from-repofile=https://pkg.cloudflare.com/cloudflared.repo
sudo dnf install cloudflared
cloudflared --version
```

Alternative without a repository: download `cloudflared-linux-x86_64.rpm` from the [GitHub releases](https://github.com/cloudflare/cloudflared/releases/latest) and install it with `sudo dnf install ./cloudflared-linux-x86_64.rpm` (no automatic updates).

**Each session:**

```bash
cloudflared tunnel --url http://localhost:8000
```

- The output shows a random `https://….trycloudflare.com` URL. That is your `SERVER_URL`.
- The URL stays valid while `cloudflared` runs. After a restart you get a new one: delete the old webhook, update `SERVER_URL`, create a new webhook (see the Week 3 README notes, steps 2–8).
- Quick tunnels are meant for testing: Cloudflare gives no uptime guarantee for them.
