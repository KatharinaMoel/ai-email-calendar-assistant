# Week 1: Project Setup

## This Week's Goals

1. Understand what we are building and why
2. Set up the tools used throughout the cohort
3. Create a local Python environment with `uv`
4. Create your own GitHub repository
5. Learn how `.env.example` protects secrets
6. Prepare a Nylas developer account for Week 2

Week 1 stops at project preparation. We will not build FastAPI, connect an email account, or create webhooks yet.

## The Project

Over the cohort, we will build an AI personal assistant for email and calendar work. Nylas will connect the application to supported providers. Later workflows will interpret incoming messages and help the user decide what to do next.

```text
Email and calendar provider
        ↓
      Nylas
        ↓
AI personal assistant
        ↓
User reviews or approves an action
```

## 1. Prerequisites

- Python 3.12 or newer
- Git
- A GitHub account
- [uv](https://docs.astral.sh/uv/)
- VS Code, Cursor, or another code editor

Confirm the command-line tools are available:

```bash
python3 --version
git --version
uv --version
```

## 2. Get the Week 1 Materials

Clone the cohort repository and switch to the Week 1 branch:

```bash
git clone https://github.com/lindseypeng/ai-personal-assistant.git
cd ai-personal-assistant
git switch week-1
```

## 3. Set Up the Python Environment

Create the virtual environment and synchronize the project:

```bash
uv venv
source .venv/bin/activate
uv sync
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

There is no application to run yet. This step confirms that Python and `uv` work before we start coding in Week 2.

## 4. Create Your Own GitHub Repository

1. Open [GitHub](https://github.com/) and select **New repository**.
2. Name it `ai-personal-assistant`.
3. Choose public or private visibility.
4. Do not initialize it with a README, license, or `.gitignore`.
5. Follow GitHub's instructions to connect your local project and push it.

For example:

```bash
git remote rename origin cohort
git remote add origin https://github.com/YOUR-USERNAME/ai-personal-assistant.git
git push -u origin main
git push -u origin week-1
```

Keeping the cohort repository as `cohort` makes it possible to fetch future teaching branches without replacing your own `origin`.

## 5. Understand `.env.example`

The repository includes `.env.example` to document settings that later weeks will require. It contains names and placeholders only.

When configuration begins, create a local copy:

```bash
cp .env.example .env
```

The `.env` file belongs only on your computer and is excluded by `.gitignore`. Never commit real API keys, access tokens, webhook secrets, or personal email content.

## Homework: Prepare Nylas for Week 2

This homework prepares the external service we will connect to in Week 2. Complete the dashboard and local configuration steps now. The authentication and webhook commands are included below as a preview, but they require application files that we will build together next week.

### 1. Create a Nylas Developer Account

1. Register for a free account at the [Nylas Dashboard](https://dashboard-v3.nylas.com/register).
2. Verify your email address and sign in.
3. Create an application named `ai-personal-assistant`.
4. Choose the API region closest to you:
   - US: `https://api.us.nylas.com`
   - EU: `https://api.eu.nylas.com`

Keep the selected region consistent throughout the project.

### 2. Find the Application Credentials

In the Nylas Dashboard, locate and record:

- the client ID
- the API key
- the API URI for the selected region

These values are secrets. Store them only in your local `.env` file. Do not paste them into Slack, screenshots, class notes, commits, or pull requests.

### 3. Prepare the Local Environment File

Create a local environment file from the template:

```bash
cp .env.example .env
```

Add the values available from the dashboard:

```env
NYLAS_CLIENT_ID=your_client_id
NYLAS_API_KEY=your_api_key
NYLAS_API_URI=https://api.eu.nylas.com
EMAIL=you@example.com
```

Use the US URI instead if the Nylas application belongs to the US region. Leave `NYLAS_GRANT_ID`, `NYLAS_WEBHOOK_SECRET`, and `SERVER_URL` empty for now.

Confirm that `.env` does not appear in the files staged for Git:

```bash
git status
```

### 4. Prepare Hosted Authentication

Hosted authentication is the Nylas login page that will let a user connect an email account without our application managing provider passwords.

In the Nylas Dashboard:

1. Open the application's hosted-authentication settings.
2. Add this callback URI:

```text
http://localhost:5010/oauth/exchange
```

3. Save the configuration.

The callback will not work yet because Week 1 does not contain an application server. We will implement it in Week 2.

### 5. Week 2 Authentication Preview

After we create the Nylas authentication helper in Week 2, the flow will be:

```text
Browser → Nylas login → callback in our application → grant ID
```

We will then run:

```bash
uv run python -m app.config.config_auth
```

and visit:

```text
http://localhost:5010/nylas/auth
```

After connecting a development email account, Nylas will return a grant ID. We will store it locally:

```env
NYLAS_GRANT_ID=your_grant_id
```

Do not run these commands in Week 1 because `app.config.config_auth` does not exist yet.

### 6. Week 2 Webhook Preview

A webhook allows Nylas to notify our application when a new email arrives:

```text
New email → Nylas → public HTTPS URL → our local application
```

Our local server will not be publicly reachable by default. In Week 2, we will create a temporary HTTPS tunnel with Pinggy:

```bash
ssh -p 443 -R0:localhost:8000 free.pinggy.io
```

We will copy the HTTPS URL that Pinggy returns into `.env`:

```env
SERVER_URL=https://your-pinggy-url
```

After building the webhook configuration script, we will register the endpoint with:

```bash
uv run python -m app.config.config_webhook
```

Nylas will return a webhook secret, which we will store locally:

```env
NYLAS_WEBHOOK_SECRET=your_webhook_secret
```

Do not create the tunnel or webhook in Week 1. The local server and webhook endpoint will be introduced first in Week 2.

### Homework Completion Criteria

By the start of Week 2:

- your Nylas developer account exists
- the `ai-personal-assistant` application exists in the dashboard
- you know whether it uses the US or EU region
- the client ID, API key, API URI, and email address are stored in your local `.env`
- the callback URI is saved in the hosted-authentication settings
- no credentials have been committed to GitHub

For additional context, read the [Nylas v3 getting-started documentation](https://developer.nylas.com/docs/v3/getting-started/).

## Week 1 Checklist

- Git, Python, and `uv` are installed
- The repository is available locally
- The virtual environment can be created successfully
- Your own GitHub repository exists and contains both branches
- You understand the purpose of `.env.example`
- Your Nylas developer application is ready for Week 2
